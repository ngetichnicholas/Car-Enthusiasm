from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Contact)

from django.contrib.gis.admin import OSMGeoAdmin

@admin.register(Car)
class CarAdmin(OSMGeoAdmin):
    list_display = ('city', 'car_location')
