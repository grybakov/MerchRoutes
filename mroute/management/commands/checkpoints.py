import requests
import json
import time

import googlemaps

from django.core.management.base import BaseCommand, CommandError
from mroute.models import MarketModel


# Чек точек на "кривые" адреса (если адрес "кривой" market_is_active = false)
# https://developers.google.com/maps/documentation/geocoding/intro
# Определение по partial_match (если  = true, значит соответствие не полное)

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('market_net', nargs='+', type=str)

    def handle(self, *args, **options):

        # Google API Key
        GOOGLE_API_KEY = 'AIzaSyA_M1UNrgnO7gOnafPEFtTwHdWozBQG5zo'

        # Checking from Directions API
        waypoints_list = []
        error_list = []

        markets = MarketModel.objects.filter(market_net=options['market_net'][0]).values_list('market_address_ru',
                                                                                              flat=True)
        ad_list = list(markets)

        for ad in ad_list:
            time.sleep(0.4)
            self.stdout.write(self.style.SUCCESS('Чекаем адрес: {0}'.format(ad)))
            gmaps = googlemaps.Client(key=GOOGLE_API_KEY)

            # Correct points
            start_point = 'Широкая ул., 9, Москва, 127282'
            finish_point = 'Краснопрудная ул., 13 Москва 107140'
            waypoints_list.append(ad)

            routes = gmaps.directions(start_point, finish_point,
                                      mode="walking",
                                      waypoints=waypoints_list,
                                      units="metric",
                                      optimize_waypoints=True)

            if not routes:
                self.stdout.write(self.style.WARNING('Ошибка! Адрес: {0} - не точное соответствие!'.format(ad)))
                error_list.append(ad)

            queryset = MarketModel.objects.filter(market_address_ru=ad).values('market_address_en')
            if queryset[0]['market_address_en'] != routes[0]['legs'][0]['end_address']:
                self.stdout.write(self.style.WARNING('Ошибка! Адрес: {0} - не точное соответствие!'.format(ad)))
                error_list.append(ad)

            waypoints_list = []

        print('ERROR: ' + str(error_list))

