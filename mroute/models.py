from django.db import models


class NetModel(models.Model):
    net_code = models.CharField(null=False, max_length=100, verbose_name='Код сети (латиница)')
    net_name = models.CharField(null=False, max_length=100, verbose_name='Название сети (кирилица)')
    net_icon_link = models.CharField(null=True, blank=True, max_length=300, verbose_name='Ссылка на иконку')
    net_icon_size_x = models.CharField(null=True, blank=True, max_length=10, verbose_name='Размер иконки по X')
    net_icon_size_y = models.CharField(null=True, blank=True, max_length=10, verbose_name='Размер иконки по Y')
    net_status = models.BooleanField(null=False, default=True, verbose_name='Статус')

    @classmethod
    def get_points_type(cls):
        POINT_TYPE = []
        for nets_param in NetModel.objects.all().values_list('net_code', 'net_name'):
            POINT_TYPE.append(nets_param)
        return tuple(POINT_TYPE)

    class Meta:
        db_table = 'Nets'


class MarketModel(models.Model):
    market_net = models.CharField(choices=NetModel.get_points_type(), null=False, max_length=400, verbose_name='Сеть')
    market_address_ru = models.CharField(null=False, max_length=400, verbose_name='Адрес (кирилица)')
    market_address_en = models.CharField(max_length=400, verbose_name='Адрес (латиница)')
    market_lat = models.FloatField(verbose_name='Координата X')
    market_lng = models.FloatField(verbose_name='Координата Y')
    market_is_active = models.BooleanField(null=False, default=True, verbose_name='Статус')

    class Meta:
        db_table = 'Markets'


class RouteModel(models.Model):
    route_name = models.CharField(null=False, max_length=400, verbose_name='Название маршрута')
    route_desc = models.TextField(max_length=500, verbose_name='Описание маршрута')
    route_rawArray = models.TextField(null=False, verbose_name='"Сырые" данные маршрута')
    route_status = models.BooleanField(null=False, default=True, verbose_name='Статус')

    class Meta:
        db_table = 'Routes'


class MetroModel(models.Model):
    metro_name_ru = models.CharField(null=False, max_length=400, verbose_name='Название станции')
    metro_lat = models.FloatField(verbose_name='Координата X')
    metro_lng = models.FloatField(verbose_name='Координата Y')
    metro_city = models.CharField(null=False, max_length=400, verbose_name='Город')
    metro_is_active = models.BooleanField(null=False, default=True, verbose_name='Статус')

    class Meta:
        db_table = 'MetroStations'

