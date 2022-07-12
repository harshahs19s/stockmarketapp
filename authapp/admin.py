from django.contrib import admin
from authapp.models import UserRegistrationModel, Order

admin.site.register(UserRegistrationModel)
admin.site.register(Order)

# Register your models here.
