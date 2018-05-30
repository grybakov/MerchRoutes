from django.test import TestCase
from django.urls import reverse

from .forms import MarketForm
from .models import MarketModel, RouteModel, MetroModel


class IndexViewTest(TestCase):

    def test_url_exists_at_desired_location(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_url_accessible_by_name(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        response = self.client.get(reverse('index'))
        self.assertTemplateUsed(response, 'index.html')


class NewsViewTest(TestCase):

    def test_url_exists_at_desired_location(self):
        response = self.client.get('/news/')
        self.assertEqual(response.status_code, 200)

    def test_url_accessible_by_name(self):
        response = self.client.get(reverse('news'))
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        response = self.client.get(reverse('news'))
        self.assertTemplateUsed(response, 'news.html')


class AddMarketViewTest(TestCase):

    correct_market = {'market_net': 'PRKRS',
                      'market_address_ru': 'Балашиха, Энтузиастов шоссе, 36, А, ТЦ "Вертикаль"',
                      'market_address_en': "Shosse Entuziastov, 36а, Balashikha, Moskovskaya oblast', Russia, 143912",
                      'market_lat': 55.793625,
                      'market_lng': 37.939151,
                      'market_is_active': True}

    def test_url_exists_at_desired_location(self):
        response = self.client.get('/addmarket/')
        self.assertEqual(response.status_code, 200)

    def test_url_accessible_by_name(self):
        response = self.client.get(reverse('addmarket'))
        self.assertEqual(response.status_code, 200)

    def test_correct_template(self):
        response = self.client.get(reverse('addmarket'))
        self.assertTemplateUsed(response, 'addmarket.html')

    def test_success_save_market(self):
        response = self.client.post(reverse('addmarket'),
                                    {'market_net': 'PRKRS',
                                     'market_address_ru': 'Балашиха, Энтузиастов шоссе, 36, А, ТЦ "Вертикаль"'})
        self.assertEqual(response.status_code, 200)
        # message
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Успешно сохранено.')
        # in BD
        market = MarketModel.objects.all()
        self.assertEqual(len(market), 1)
        self.assertEqual(market[0].market_address_en, self.correct_market['market_address_en'])
        self.assertEqual(market[0].market_lat, self.correct_market['market_lat'])
        self.assertEqual(market[0].market_lng, self.correct_market['market_lng'])
        self.assertEqual(market[0].market_is_active, self.correct_market['market_is_active'])

    def test_fail_save_market_incorrect_market_net(self):
        response = self.client.post(reverse('addmarket'),
                                    {'market_net': 'test',
                                     'market_address_ru': 'Балашиха, Энтузиастов шоссе, 36, А, ТЦ "Вертикаль"'})
        self.assertEqual(response.status_code, 200)
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Форма заполнена не верно! Заполните заново или обратитесь к Администратору.')
        # in BD
        market = MarketModel.objects.all()
        self.assertEqual(len(market), 0)

    def test_fail_save_market_incorrect_market_address_ru(self):
        response = self.client.post(reverse('addmarket'),
                                    {'market_net': 'PRKRS', 'market_address_ru': 'д. Нереальная д.666'})
        self.assertEqual(response.status_code, 200)
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'При сохранении произошла ошибка. Обратитесь к Администратору.')
        # in BD
        market = MarketModel.objects.all()
        self.assertEqual(len(market), 0)

    def test_form_exists_in_context(self):
        response = self.client.get(reverse('addmarket'))
        self.assertTrue(response.context['form'])


class MarketTranslitViewTest(TestCase):

    fixtures = ['markets.json']
    correct_market = {'Ulitsa Onezhskaya, 34, Moskva, Russia, 125413': 'г. Москва, Онежская Улица, д. 34',
                      'Yasnogorskaya Ulitsa, 2, Moskva, Russia, 117588': 'Москва, Ясногорская ул., д. 2',
                      'Prokatnaya Ulitsa, 2, Moskva, Russia, 111555': 'г. Москва, ул. Прокатная, д. 2'}

    def test_url_exists_at_desired_location(self):
        response = self.client.post('/marketTranslit/', {'data[]': self.correct_market.keys()})
        self.assertEqual(response.status_code, 200)

    def test_url_accessible_by_name(self):
        response = self.client.post(reverse('marketTranslit'), {'data[]': self.correct_market.keys()})
        self.assertEqual(response.status_code, 200)

    def test_success_translit(self):
        response = self.client.post(reverse('marketTranslit'), {'data[]': self.correct_market.keys()})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'OK')
        self.assertEqual(response.json()['data'], self.correct_market)


class GetAllMarketsViewTest(TestCase):

    fixtures = ['markets.json']
    correct_market = 'г. Москва, Онежская Улица, д. 34'

    def test_url_exists_at_desired_location(self):
        response = self.client.post('/getAllMarkets/')
        self.assertEqual(response.status_code, 200)

    def test_url_accessible_by_name(self):
        response = self.client.post(reverse('getAllMarkets'))
        self.assertEqual(response.status_code, 200)

    def test_success_get_all_active_markets(self):
        response = self.client.post(reverse('getAllMarkets'))
        self.assertEqual(len(response.json()), 1038)
        self.assertTrue(self.correct_market in set(response.json()))

    def test_market_not_included_if_active_is_false(self):

        market = 'Ulitsa Onezhskaya, 34, Moskva, Russia, 125413'

        queryset = MarketModel.objects.get(market_address_en=market)
        queryset.market_is_active = False
        queryset.save()

        response = self.client.post(reverse('getAllMarkets'))
        self.assertEqual(len(response.json()), 1037)
        self.assertFalse(self.correct_market in set(response.json()))


class GetMarketsViewTest(TestCase):

    fixtures = ['markets.json']
    correct_market = 'г. Москва, Онежская Улица, д. 34'

    def test_url_exists_at_desired_location(self):
        response = self.client.get('/getMarkets/', {'NET': 'DKS'})
        self.assertEqual(response.status_code, 200)

    def test_url_accessible_by_name(self):
        response = self.client.get(reverse('getMarkets'), {'NET': 'DKS'})
        self.assertEqual(response.status_code, 200)

    def test_success_get_active_markets_of_net(self):
        response = self.client.get(reverse('getMarkets'), {'NET': 'DKS'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'OK')
        self.assertEqual(len(response.json()['data']), 406)
        for mk in response.json()['data']:
            self.assertEqual(mk['market_net'], 'DKS')
            self.assertEqual(mk['market_is_active'], True)

    def test_market_of_net_not_included_if_active_is_false(self):

        market = 'Zyuzinskaya Ulitsa, 3, Moskva, Russia, 117418'

        queryset = MarketModel.objects.get(market_address_en=market)
        queryset.market_is_active = False
        queryset.save()

        response = self.client.get(reverse('getMarkets'), {'NET': 'DKS'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'OK')
        self.assertEqual(len(response.json()['data']), 405)
        for mk in response.json()['data']:
            self.assertNotEqual(mk['market_address_en'], market)


class MakeRouteFixStartViewTest(TestCase):

    fixtures = ['markets.json', 'metro.json']
    test_day = {'sendDay': 'Вторник',
                'pointsArray[]': ['г. Москва, ул. Академика Варги д.8 корп.1 ТК "Лейпциг"',
                                  'Москва, ул.Профсоюзная, д.98, корп.1',
                                  'Москва, ул. Бутлерова, д. 24В',
                                  'Москва, ул.Профсоюзная, д.152, к.2, стр.2',
                                  'Москва, ул.Академика Варги, д.4А']}

    correct_test_route = ['улица Академика Варги, 8, корп. 1, Москва, г. Москва, Russia, 117133',
                          'Ulitsa Akademika Vargi, 4А, Moskva, Russia, 117133',
                          'Profsoyuznaya Ulitsa, 152 корпус 2, Moskva, Russia, 117321',
                          'Profsoyuznaya Ulitsa, 98 корпус 1, Moskva, Russia, 117485',
                          'Ulitsa Butlerova, 24В, Moskva, Russia, 117342']

    def test_success_calculation_route(self):
        response = self.client.get(reverse('makeRouteFixStart'), self.test_day)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'OK')

        google_response = response.json()['data'][0]['legs']
        for count_id, leg in enumerate(google_response):
            self.assertEqual(leg['start_address'], self.correct_test_route[count_id])
        self.assertEqual(google_response[3]['end_address'], self.correct_test_route[4])


class MakeRouteAutoStartViewTest(TestCase):

    fixtures = ['markets.json', 'metro.json']
    test_day = {'sendDay': 'Среда',
                'pointsArray[]': ['г. Москва, Люблинская Улица, д. 169, корп. 2, ТЦ "МариЭль"',
                                  'г. Москва, ул. Краснодарская, д. 57, корп. 1',
                                  'Москва, Краснодарская, 51, к. 2',
                                  'г. Москва, Братиславская Улица, д. 12',
                                  'г. Москва, Новочеркасский бульвар, д. 41, корп. 4',
                                  'г. Москва, Братиславская Улица, д. 27, корп. 1',
                                  'г. Москва, ул. Братиславская, д. 30']}

    correct_test_route = ['Krasnodarskaya Ulitsa, 51 корпус 2, Moskva, Russia, 109559',
                          'Krasnodarskaya Ulitsa, 57 корпус 1, Moskva, Russia, 109559',
                          'Bratislavskaya Ulitsa, 12, Moskva, Russia, 109451',
                          'Bratislavskaya Ulitsa, 27 к 1, Moskva, Russia, 109469',
                          'Bratislavskaya Ulitsa, 30, Moskva, Russia, 109469',
                          'Lyublinskaya Ulitsa, 169 к2, Moskva, Russia, 109652',
                          "Novocherkasskiy Bul'var, 41 корпус 4, Moskva, Russia, 109369"]

    def test_success_calculation_route(self):
        response = self.client.get(reverse('makeRouteAutoStart'), self.test_day)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'OK')
        self.assertEqual(response.json()['day'], self.test_day['sendDay'])

        google_response = response.json()['data'][0]['legs']
        # for i in google_response:
        #     print(i['start_address'])

        for count_id, leg in enumerate(google_response):
            print('{0} - {1}'.format(leg['start_address'], self.correct_test_route[count_id]))
            # self.assertEqual(leg['start_address'], self.correct_test_route[count_id])
        self.assertEqual(google_response[5]['end_address'], self.correct_test_route[6])


class MakeXlsReportViewTest(TestCase):

    def test_url_exists_at_desired_location(self):
        response = self.client.get('/getMarkets/', {'NET': 'DKS'})
        self.assertEqual(response.status_code, 200)

    def test_url_accessible_by_name(self):
        response = self.client.get(reverse('getMarkets'), {'NET': 'DKS'})
        self.assertEqual(response.status_code, 200)

