import io
import sys
import copy
import json
import base64
import math

import xlsxwriter
import googlemaps

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.contrib import messages

from .models import MarketModel, RouteModel, MetroModel
from .forms import MarketForm


# Google API Key
GOOGLE_API_KEY = 'AIzaSyA_M1UNrgnO7gOnafPEFtTwHdWozBQG5zo'
GOOGLE_API_KEY_GEOCODE = 'AIzaSyAPGRaziW2AmkRSTgfvaKB7Ddw-cgaMGUQ'


def index(request):
    return render(request, 'index.html')


def news(request):
    return render(request, 'news.html')


def addmarket(request):

    if request.method == 'POST':
        form = MarketForm(request.POST)
        if form.is_valid():
            market = form.save(commit=False)
            # GEO
            gmaps = googlemaps.Client(key=GOOGLE_API_KEY_GEOCODE)
            geocode_result = gmaps.geocode(request.POST['market_address_ru'])
            if geocode_result != []:
                market.market_address_en = geocode_result[0]['formatted_address']
                market.market_lat = geocode_result[0]['geometry']['location']['lat']
                market.market_lng = geocode_result[0]['geometry']['location']['lng']
                market.market_is_active = True
                market.save()
                messages.success(request, 'Успешно сохранено.')
            else:
                messages.error(request, 'При сохранении произошла ошибка. Обратитесь к Администратору.')
        else:
            messages.error(request, 'Форма заполнена не верно! Заполните заново или обратитесь к Администратору.')
    else:
        form = MarketForm()
    return render(request, 'addmarket.html', {'form': form})


@csrf_exempt
# TODO require_http_methods
def marketTranslit(request):

    translitArray = {}
    req_dict = dict(request.POST)
    rlist = req_dict.get('data[]')
    for i in range(len(rlist)):
        addr = rlist[i]
        queryset = MarketModel.objects.filter(market_address_en=addr).values('market_address_ru')
        translitArray[addr] = queryset[0]['market_address_ru']
    response = {'data': translitArray, 'status': 'OK'}
    print(response)
    return JsonResponse(response)


# Отдает вообще все адреса точек (для выпадающего списка)
def getAllMarkets(request):

    queryset = MarketModel.objects.filter(market_is_active=True).values_list('market_address_ru', flat=True)
    json_list = []
    for i in queryset:
        json_list.append(i)
    return JsonResponse(json_list, safe=False)


# Отдает все точки запрошенной сети (фильтр для Google Maps).
def getMarkets(request):

    queryset = MarketModel.objects.filter(market_is_active=True, market_net=request.GET['NET']).values()
    response = {'data': list(queryset), 'status': 'OK'}
    return JsonResponse(response)


# Создание маршрутов по известной начальной точке.
def makeRouteFixStart(request):

    min_time = sys.maxsize

    req_dict = dict(request.GET)

    load_day = req_dict['sendDay'][0]
    load_points = req_dict['pointsArray[]']

    start_point = load_points.pop(0)
    all_points = load_points

    for finish_point in all_points:
        waypoints_list = copy.deepcopy(all_points)
        waypoints_list.remove(finish_point)
        # Просим Google дать данные по маршруту
        gmaps = googlemaps.Client(key=GOOGLE_API_KEY)
        routes = gmaps.directions(start_point, finish_point,
                                  mode="walking",
                                  waypoints=waypoints_list,
                                  units="metric",
                                  optimize_waypoints=True)

        # TODO глянуть логгирование после выкладки
        # Бага из-за Варшавское шоссе, 21-й км, Москва, 117405

        count_time = 0
        for w in range(len(routes[0]['legs'])):
            value = routes[0]['legs'][w]['duration']['value']
            count_time = count_time + value
        if count_time < min_time:
            min_time = count_time
            bestRoutes = routes
            continue

    response = {'day': load_day, 'data': bestRoutes, 'status': 'OK'}
    return JsonResponse(response)


# Создает марщруты с автоматическим определением стартовой точки возле ближайшего метро.
def makeRouteAutoStart(request):

    MAX_METRO_R = 0.7  # Км

    # Счетчики перебора
    min_time_iter = sys.maxsize
    min_time_total = sys.maxsize
    # Оптимальный маршрут
    total_goolist = []

    req_dict = dict(request.GET)

    load_day = req_dict['sendDay'][0]
    load_points = req_dict['pointsArray[]']

    metro_dict = MetroModel.objects.filter(metro_is_active=True).values()

    # Получаем координаты точек маршрута из БД и укладываем в geo_list
    geo_list = []
    for point in load_points:
        geo_dict = {}
        geo_dict.fromkeys(['address', 'point_lat', 'point_lng'])
        geo_dict['address'] = point
        queryset = MarketModel.objects.filter(market_address_ru=point).values()
        geo_dict['point_lat'] = queryset[0]['market_lat']
        geo_dict['point_lng'] = queryset[0]['market_lng']
        geo_list.append(geo_dict)

    # Поиск возможных стартовых точек в заданном радиусе MAX_METRO_R
    start_points_list = []
    for goo in geo_list:
        lat0 = goo['point_lat']
        lon0 = goo['point_lng']
        for m in metro_dict:
            lat = m['metro_lat']
            lon = m['metro_lng']
            p = 0.017453292519943295  # Math.PI / 180
            a = 0.5 - math.cos((lat - lat0) * p) / 2 + math.cos(lat0 * p) * math.cos(lat * p) * (1 - math.cos((lon - lon0) * p)) / 2
            ss = 12742 * math.asin(math.sqrt(a))  # 2 * R; R = 6371 km
            if MAX_METRO_R >= ss:
                start_points_list.append(goo)

    # Если не найдено ни одной стартовой точки в пределах MAX_METRO_R, завершаем работу
    if not start_points_list:
        response = {'day': load_day, 'error_massage': 'В пределах заданного радиуса ({0} км.) не удалось найти ни одной'
                                                      ' стартовой точки.'.format(MAX_METRO_R), 'status': 'Fail'}
        return JsonResponse(response)

    # Подготавливаем списки точек
    # other_list - все адреса, sort_start_points_list - адреса стартовых точек
    other_list = []
    for d in geo_list:
        other_list.append(d['address'])

    sort_start_points_list = []
    for j in start_points_list:
        sort_start_points_list.append(j['address'])

    # Опрашиваем Google на предмет оптимального маршрута
    for e in sort_start_points_list:
        routes = 0
        start_point = e
        new_all_points = copy.deepcopy(other_list)
        new_all_points.remove(start_point)
        for a in new_all_points:
            finish_point = a
            d_points = copy.deepcopy(new_all_points)
            d_points.remove(finish_point)
            waypoints_list = d_points
            # Просим Google дать данные по маршруту
            gmaps = googlemaps.Client(key=GOOGLE_API_KEY)
            routes = gmaps.directions(start_point, finish_point,
                                      mode="walking",
                                      waypoints=waypoints_list,
                                      units="metric",
                                      optimize_waypoints=True)

            count_time = 0
            # Получаем общее время
            for w in range(len(routes[0]['legs'])):
                value = routes[0]['legs'][w]['duration']['value']
                count_time = count_time + value
            # Поиск минимального в итерации
            if count_time < min_time_iter:
                min_time_iter = count_time

        iter_goolist = routes

        # Поиск минимального во всех итерациях
        if min_time_iter < min_time_total:
            min_time_total = min_time_iter
            # Сохраняем оптимальный маршрут
            total_goolist = iter_goolist

    response = {'day': load_day, 'data': total_goolist, 'status': 'OK'}
    return JsonResponse(response)


@csrf_exempt
# Выгрузка рассчитанного маршрута в xls (на вход приходит bigArrayNorm)
def makeXlsReport(request):

    if request.method == 'POST':
        rawArray = json.loads(request.body)
        # Формируем ответ
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="Routes.xlsx"'
        xlsx_data = WriteToExcel(rawArray)
        response.write(xlsx_data)
        return response


def WriteToExcel(rawArray):

    TITLE_ROUTE = ['Начальная точка',
                   'Конечная точка',
                   'Расстояние',
                   'Время, дол.ед.',
                   'Время, мин']

    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    title_format = workbook.add_format({'bold': True})

    for ent in rawArray:
        worksheet_day = workbook.add_worksheet(ent['day'])
        # Заголовки
        for col_id, entry in enumerate(TITLE_ROUTE):
            worksheet_day.write(0, col_id, entry, title_format)
        # Данные
        for row_id, qw in enumerate(ent['calc_result']['legs'], start=1):
            transDict = dict(ent['translitDict'])
            ru_start = transDict[qw['start_address']]
            ru_stop = transDict[qw['end_address']]
            worksheet_day.write(row_id, 0, ru_start)
            worksheet_day.write(row_id, 1, ru_stop)
            worksheet_day.write(row_id, 2, qw['distance']['text'])
            worksheet_day.write(row_id, 3, qw['duration']['value'] / 3600)
            worksheet_day.write(row_id, 4, qw['duration']['text'])

    workbook.close()
    xlsx_data = output.getvalue()
    # base64
    xlsx_encode = base64.encodebytes(xlsx_data)
    return xlsx_encode

