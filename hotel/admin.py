from django.contrib import admin

from hotel.models import *
# Register your models here.

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display=['number', 'description', 'price']

@admin.register(Accomodattion)
class AccomodattionAdmin(admin.ModelAdmin):
    list_display=['id', 'in_date', 'out_date', 'price', 'room']

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display=['id', 'name', 'price']

@admin.register(Provision)
class ProvisionAdmin(admin.ModelAdmin):
    list_display=['id', 'quantity', 'price']