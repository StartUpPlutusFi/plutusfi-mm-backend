from pydoc import describe
from xmlrpc.client import Boolean
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.utils.translation import gettext as _

from apps.account.models import User


class Exchange(models.Model):

    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ApiKeys(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    api_key = models.CharField(_("API KEY"), max_length=200)
    api_secret = models.CharField(_("API SECRET"), max_length=200)
    description = models.CharField(_("Description"), max_length=255)
    default = models.BooleanField(default=False)
    exchange = models.ForeignKey(Exchange, on_delete=models.DO_NOTHING, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.description

    class Meta:

        db_table = "api_keys_store"


class DashboardSysLogs(models.Model):
    action = models.CharField(max_length=64)
    data = models.TextField(max_length=256)
    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:

        db_table = "dashboard_sys_logs"


class BotConfigPairtokens(models.Model):

    pair = models.CharField("token", max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.pair

    class Meta:
        db_table = "bot_config_pairtokens"


class MarketMakerBot(models.Model):

    name = models.CharField(max_length=32)
    description = models.CharField(max_length=256)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    api_key = models.ForeignKey(ApiKeys, on_delete=models.DO_NOTHING)
    pair_token = models.ForeignKey(
        BotConfigPairtokens,
        on_delete=models.DO_NOTHING,
        verbose_name=_("Token pair"),
    )
    user_ref_price = models.FloatField(default=0)
    side = models.IntegerField(default=0, max_length=1)
    trade_candle = models.IntegerField(default=10)
    trade_amount = models.FloatField(default=0)
    status = models.CharField(max_length=16, default="STOP")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def api(self):
        return self.api_key.name

    def __str__(self):
        return self.name

    class Meta:
        db_table = "market_maker_bot"


class MarketMakerBotOrderHistory(models.Model):

    bot = models.ForeignKey(MarketMakerBot, models.DO_NOTHING, blank=True, null=True)
    pair_token = models.CharField(max_length=16, default="DUMMY_TK")
    spreed = models.IntegerField(default=0)
    status = models.CharField(max_length=16, default="STOP")
    side = models.CharField(max_length=4)
    trade_qty_low = models.IntegerField(default=0)
    trade_qty_high = models.IntegerField(default=0)
    trade_candle = models.IntegerField(default=0)
    trade_amount = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.bot.id)

    class Meta:
        db_table = "market_maker_bot_order_history"


class MarketMakerBotAutoTradeQueue(models.Model):

    bot = models.ForeignKey(MarketMakerBot, models.DO_NOTHING, blank=True, null=True)
    price = models.FloatField(default=0)
    quantity = models.FloatField(default=0)
    side = models.CharField(default="FILL")
    status = models.CharField(default="FINISHED")
    candle = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.bot.id)
    
    class Meta:
        db_table = "dashboard_marketmakerbotautotradequeue"


        


class BidBot(models.Model):

    name = models.CharField(max_length=32, default="None")
    description = models.CharField(max_length=256, default="None")
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    api_key = models.ForeignKey(ApiKeys, on_delete=models.DO_NOTHING)
    pair_token = models.ForeignKey(
        BotConfigPairtokens,
        on_delete=models.DO_NOTHING,
        verbose_name=_("Token pair"),
        default=1,
    )
    order_size = models.IntegerField(default=0)
    number_of_orders = models.IntegerField(default=0)
    budget = models.FloatField(default=0)
    trade_amount = models.FloatField(default=0)
    status = models.CharField(max_length=16, default="STOP")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = "market_maker_bid_bot"


class BidBotOrderHistory(models.Model):
    bid_bot = models.ForeignKey(BidBot, models.DO_NOTHING, blank=True, null=True)
    pair_token = models.CharField(max_length=16, default="DUMMY_TK")
    order_size = models.IntegerField(default=0)
    number_of_orders = models.IntegerField(default=0)
    budget = models.FloatField(default=0)
    trade_amount = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = "bid_bot_order_history"


class CancelOrderBookBID(models.Model):
    bid_bot = models.ForeignKey(BidBot, models.DO_NOTHING, blank=True, null=True)
    cancel_order_list = models.CharField(max_length=512)
    order_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = "cancel_order_book_bid_bot"


class CancelOrderBookBot(models.Model):
    bot = models.ForeignKey(MarketMakerBot, models.DO_NOTHING, blank=True, null=True)
    cancel_order_id = models.CharField(max_length=64)
    order_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.cancel_order_id)

    class Meta:
        db_table = "cancel_order_book_mm_bot"
