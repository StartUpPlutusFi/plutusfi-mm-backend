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
