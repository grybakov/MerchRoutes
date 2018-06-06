from django import forms

from .models import MarketModel, RouteModel


class MarketForm(forms.ModelForm):
    class Meta:
        model = MarketModel
        fields = ('market_net', 'market_address_ru',)


class SaveRouteForm(forms.ModelForm):
    class Meta:
        model = RouteModel
        fields = ('route_name', 'route_desc', 'route_rawArray',)
        widgets = {
            'route_rawArray': forms.HiddenInput()
        }

