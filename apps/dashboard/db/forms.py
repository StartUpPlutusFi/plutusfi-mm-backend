from django import forms
from apps.dashboard.db.models import *


class ApiForm(forms.ModelForm):
    exchange = forms.ModelChoiceField(queryset=Exchange.objects.all())
    description = forms.CharField(max_length=128, required=True)
    api_key = forms.CharField(max_length=1024, required=True)
    api_secret = forms.CharField(max_length=1024, required=True)
    default = forms.BooleanField(required=False)

    class Meta:
        model = ApiKeys
        fields = ["description", "api_key", "api_secret", "default", "exchange"]
        exclude = ("user",)


class BotForm(forms.ModelForm):

    CHOICES = (
        (1, "1 s"),
        (5, "5 s"),
        (10, "10 s"),
        (30, "30 s"),
        (60, "1 Min"),
        (300, "5 Min"),
        (600, "10 Min"),
        (1800, "30 Min"),
        (3600, "1 H"),
    )

    name = forms.CharField(max_length=32)
    description = forms.CharField(max_length=256)
    api_key = forms.ModelChoiceField(queryset=ApiKeys.objects.all())
    pair_token = forms.ModelChoiceField(queryset=BotConfigPairtokens.objects.all())
    trade_qty_range_low = forms.FloatField()
    trade_qty_range_high = forms.FloatField()
    trade_candle = forms.ChoiceField(choices=CHOICES)
    trade_amount = forms.FloatField()

    class Meta:
        model = MarketMakerBot
        fields = [
            "name",
            "description",
            "api_key",
            "pair_token",
            "trade_qty_range_low",
            "trade_qty_range_high",
            "trade_candle",
            "trade_amount",
        ]
        exclude = ("user",)


class BidForm(forms.ModelForm):
    name = forms.CharField()
    description = forms.CharField()
    api_key = forms.ModelChoiceField(queryset=ApiKeys.objects.all())
    pair_token = forms.ModelChoiceField(queryset=BotConfigPairtokens.objects.all())
    trade_amount = forms.FloatField(required=False)
    budget = forms.FloatField()
    order_size = forms.IntegerField()
    number_of_orders = forms.IntegerField()

    class Meta:
        model = BidBot
        fields = [
            "name",
            "description",
            "api_key",
            "pair_token",
            "trade_amount",
            "order_size",
            "number_of_orders",
            "budget",
        ]
        exclude = ("user",)
