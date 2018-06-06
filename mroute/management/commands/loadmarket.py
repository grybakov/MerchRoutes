import os
import googlemaps

from django.core.management.base import BaseCommand, CommandError
from mroute.models import MarketModel


# Загрузчик магазинов из файла TXT. Обязательно указывать сеть магазина!

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('market_file', nargs='+', type=str)

    def handle(self, *args, **options):

        # https://developers.google.com/maps/documentation/geocoding/intro

        GOOGLE_API_KEY_GEOCODE = 'AIzaSyA_M1UNrgnO7gOnafPEFtTwHdWozBQG5zo'
        NET = ''

        error_count = 0
        error_array = []
        success_count = 0

        pyth_file = os.getcwd() + '\\' + options['market_file'][0]
        with open(pyth_file, 'r') as file_list:
            for addr in file_list:
                # Удаление пробелов в начале и в конце и переносы строк!
                addr = addr.strip(' \n\t\r')
                # Получаем координаты точек маршрута через GOOGLE GEOCODE и укладываем в geo_list
                geo_req = googlemaps.Client(key=GOOGLE_API_KEY_GEOCODE)
                geo_point = geo_req.geocode(addr)
                if geo_point != []:
                    market = MarketModel(market_net=NET, market_address_ru=addr,
                                         market_address_en=geo_point[0]['formatted_address'],
                                         market_lat=geo_point[0]['geometry']['location']['lat'],
                                         market_lng=geo_point[0]['geometry']['location']['lng'],
                                         market_is_active=True)
                    market.save()
                    self.stdout.write(self.style.SUCCESS('Адрес: {0} - успешно добавлен в БД'.format(addr)))
                    success_count = success_count + 1
                else:
                    self.stdout.write(self.style.WARNING('Ошибка! Адрес: {0}. Статус: {1}'.format(addr, geo_point['status'])))
                    error_count = error_count + 1
                    error_array.append(addr)

        print('Итого загружено: успешно - {0}, ошибка - {1}'.format(success_count, error_count))
        print('Адреса загруженные с ошибкой: {0}'.format(str(error_array)))

