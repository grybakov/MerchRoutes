from django import forms

from .models import MarketModel


class MarketForm(forms.ModelForm):
    class Meta:
        model = MarketModel
        fields = ('market_net', 'market_address_ru',)

