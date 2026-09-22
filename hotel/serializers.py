from rest_framework import serializers
from django.contrib.auth.models import User
from hotel.models import *

class ServiceSerializer (serializers. ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

class RoomSerializer (serializers. ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

class ProvisionSerializer (serializers. ModelSerializer):
    class Meta:
        model = Provision
        fields = '__all__'

class AccomodattionSerializer (serializers. ModelSerializer):

    class Meta:
        model = Accomodattion
        fields = '__all__'

class UserSerializer (serializers. ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'
