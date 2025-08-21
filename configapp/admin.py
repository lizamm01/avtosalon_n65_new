from django.contrib import admin
from .models import Autosalon, Car, Brand

admin.site.register([Autosalon, Car, Brand])
