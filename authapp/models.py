from django.db import models
from django.conf import settings
# Create your models here.


class UserRegistrationModel(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    angelonestatus = models.IntegerField(default=0)  # 0 loggedout, 1 loggedin
    token = models.CharField(max_length=250, blank=True,null=True)
    client_code = models.CharField(max_length=50, blank=True,null=True)
    angelname = models.CharField(max_length=100, blank=True,null=True)
    password = models.CharField(max_length=100, blank=True,null=True)
    angelmobile = models.CharField(max_length=50, blank=True,null=True)
    angelemail = models.CharField(max_length=50, blank=True,null=True)

    def __str__(self):
        return self.user.username


class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    symbol = models.CharField(max_length=50)
    token = models.CharField(max_length=50)
    exc = models.CharField(max_length=50)
    ttype = models.CharField(max_length=50)
    number = models.CharField(max_length=50)
    profit = models.CharField(max_length=50)
    limitvalue = models.CharField(max_length=50)
    sl = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    name_ltp = models.CharField(max_length=50)
    symbol_ltp = models.CharField(max_length=50)
    amount = models.CharField(max_length=50)
    result = models.CharField(max_length=300)

    def __str__(self):
        return str(self.id)


class stockDetails(models.Model):
    token = models.CharField(max_length=50)
    symbol = models.CharField(max_length=50)
    expiry = models.CharField(max_length=50)
    strike = models.CharField(max_length=50)
    lotsize = models.CharField(max_length=50)
    instrumenttype = models.CharField(max_length=50)
    exch_seg = models.CharField(max_length=50)
    tick_size = models.CharField(max_length=50)

    def __str__(self):
        return self.id






