from django.db import models


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
    )
    market_net = models.CharField(choices=POINT_TYPE, null=False, max_length=400, verbose_name='Сеть')
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

    # Маршрут понедельника
    # route_mon = models.ManyToManyField(MarketModel, related_name='route_mon')
    # route_mon_order = models.CharField(max_length=400)
    # route_mon_status = models.BooleanField(default=True)
    # Маршрут вторника
    # route_tue = models.ManyToManyField(MarketModel, related_name='route_tue')
    # route_tue_order = models.CharField(max_length=400)
    # route_tue_status = models.BooleanField(default=True)
    # Маршрут среды
    # route_wed = models.ManyToManyField(MarketModel, related_name='route_wed')
    # route_wed_order = models.CharField(max_length=400)
    # route_wed_status = models.BooleanField(default=True)
    # Маршрут четверга
    # route_thu = models.ManyToManyField(MarketModel, related_name='route_thu')
    # route_thu_order = models.CharField(max_length=400)
    # route_thu_status = models.BooleanField(default=True)
    # Маршрут пятницы
    # route_fri = models.ManyToManyField(MarketModel, related_name='route_fri')
    # route_fri_order = models.CharField(max_length=400)
    # route_fri_status = models.BooleanField(default=True)
    # Маршрут субботы
    # route_sat = models.ManyToManyField(MarketModel, related_name='route_sat')
    # route_sat_order = models.CharField(max_length=400)
    # route_sat_status = models.BooleanField(default=False)
    # Маршрут воскресенья
    # route_sun = models.ManyToManyField(MarketModel, related_name='route_sun')
    # route_sun_order = models.CharField(max_length=400)
    # route_sun_status = models.BooleanField(default=False)

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

