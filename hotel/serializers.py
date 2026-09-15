from rest_framework import serializers
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
    #room = RoomSerializer(read_only=True)

    class Meta:
        model = Accomodattion
        fields = '__all__'
