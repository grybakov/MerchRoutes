import os
import sys
import googlemaps
import requests

from django.core.management.base import BaseCommand, CommandError
from mroute.models import MetroModel


# Загрузчик станций метро - используем HH.ru API
# Перед загрузкой очищается MetroModel!

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('CityID', nargs='+', type=int)

    def handle(self, *args, **options):
        city = {1: 'Москва', 2: 'Санкт-Петербург', 3: 'Екатеринбург', 4: 'Новосибирск'}

        MetroModel.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('MetroModel успешно очистен!'))

        # Получаем координаты станций метро от HH.ru
        cID = options['CityID'][0]
        try:
            s = requests.get('https://api.hh.ru/metro/{0}'.format(str(cID)))
            metro = s.json()  # dict от HH
            self.stdout.write(self.style.SUCCESS('Координаты станций метро успешно получены!'))
        except:
            self.stdout.write(self.style.WARNING('Ошибка при получении станций метро!\n'
                                                 'Ответ json: {0}'.format(str(s.json()))))
            sys.exit()
        else:
            metro_list = []
            for r in range(len(metro['lines'])):
                for rm in metro['lines'][r]['stations']:
                    market = MetroModel(metro_name_ru=rm['name'], metro_lat=rm['lat'], metro_lng=rm['lng'],
                                        metro_city=city[cID], metro_is_active=True)
                    market.save()
                    metro_list.append(rm)
                    self.stdout.write(self.style.SUCCESS('Успешно занесено в БД: {0}'.format(rm['name'])))
            self.stdout.write(self.style.SUCCESS('Успешно завершено! Получено станций метро: ' + str(len(metro_list))))

