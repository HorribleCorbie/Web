from rest_framework import serializers
from django.contrib.auth.models import User
from hotel.models import *
from hotel.services import *

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

    def create(self, validated_data):
        return createProvision(validated_data)

    def update(self, instance, validated_data):
        return updateProvision(instance, validated_data)

class AccomodattionSerializer (serializers. ModelSerializer):

    class Meta:
        model = Accomodattion
        fields = '__all__'

    def create(self, validated_data):
        return createAccomodattiom(validated_data)

    def update(self, instance, validated_data):
        return updateAccomodattiom(instance, validated_data)

class UserSerializer (serializers. ModelSerializer):
    role = serializers.IntegerField(source='profile.role', read_only=True)

    class Meta:
        model = User
        fields = '__all__'
