from django.contrib import admin
from .models import MarketModel, RouteModel, MetroModel


@admin.register(MarketModel)
class MarketAdmin(admin.ModelAdmin):
    list_display = ('market_net', 'market_address_ru', 'market_is_active')
    search_fields = ['market_address_ru', 'market_address_en']
    list_filter = ['market_net', 'market_is_active']


@admin.register(RouteModel)
class MarketAdmin(admin.ModelAdmin):
    # list_display = ('market_net', 'market_address_ru', 'market_is_active')
    pass


@admin.register(MetroModel)
class MarketAdmin(admin.ModelAdmin):
    list_display = ('metro_name_ru', 'metro_city', 'metro_is_active')
