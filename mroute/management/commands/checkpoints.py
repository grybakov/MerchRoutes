import os
import requests

from django.core.management.base import BaseCommand, CommandError
from mroute.models import MarketModel


# Чек точек на "кривые" адреса (если адрес "кривой" market_is_active = false)
# https://developers.google.com/maps/documentation/geocoding/intro
# Определение по partial_match (если  = true, значит соответствие не полное)

class Command(BaseCommand):

    test_data = ['', '', '', '', ]

    def add_arguments(self, parser):
        parser.add_argument('market_file', nargs='+', type=str)

    def handle(self, *args, **options):

        GOOGLE_API_KEY_GEOCODE = 'AIzaSyA_M1UNrgnO7gOnafPEFtTwHdWozBQG5zo'

        # TODO checking incorrect points

        """pyth_file = os.getcwd() + '\\' + options['market_file'][0]
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
                    error_array.append(addr) """



