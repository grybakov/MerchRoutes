from django.db import models


"""class NetModel(models.Model):
    net_code = models.CharField(null=False, max_length=100, verbose_name='Код сети (латиница)')
    net_name = models.CharField(null=False, max_length=100, verbose_name='Название сети (кирилица)')
    net_status = models.BooleanField(null=False, default=True, verbose_name='Статус')

    class Meta:
        db_table = 'Nets' """


class MarketModel(models.Model):

    POINT_TYPE = (
        ('DKS', 'Дикси'),
        ('PRKRS', 'Перекресток'),
        ('VKTR', 'Виктория'),
        ('BLL', 'BILLA'),
        ('KRS', 'Карусель'),
        ('HZ', 'ТД "Холдинг-Центр"'),
        ('MGT', 'Магнит'),
        ('PTRK', 'Пятерочка'),
        ('LNT', 'Лента'),
    )
    market_net = models.CharField(choices=POINT_TYPE, null=False, max_length=400, verbose_name='Сеть')
    # market_net = models.ForeignKey(NetModel, on_delete=models.PROTECT)
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

