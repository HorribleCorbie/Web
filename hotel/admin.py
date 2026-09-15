from django.contrib import admin

from hotel.models import *
# Register your models here.
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display=['number', 'description', 'price']

@admin.register(Accomodattion)
class AccomodattionAdmin(admin.ModelAdmin):
    list_display=['id', 'in_date', 'out_date', 'price', 'room']