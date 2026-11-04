from rest_framework import serializers
from django.contrib.auth.models import User
from hotel.models import *
from hotel.services import *

class ImageSerializer(serializers.ModelSerializer):
    room = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all().order_by('number'), style={'base_template': 'input.html'})
    class Meta:
        model = Image
        fields = '__all__'
        read_only_fields = ['user']

class ServiceSerializer (serializers. ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True, allow_null=True)
    class Meta:
        model = Service
        fields = '__all__'
        read_only_fields = ['user']

class RoomSerializer (serializers. ModelSerializer):
    picture = ImageSerializer(many=True, read_only=True)
    user_id = serializers.ReadOnlyField(source='user.id')
    user_name = serializers.CharField(source='user.username', read_only=True, allow_null=True)
    user_first_name = serializers.CharField(source='user.first_name', read_only=True, allow_null=True)
    
    def create(self, validated_data):
        if 'request' in self.context:
            validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    
    class Meta:
        model = Room
        fields = '__all__'
        read_only_fields = ['user']

class AccomodattionShortSerializer(serializers.ModelSerializer):
    client_id = serializers.ReadOnlyField(source='client.id')
    client_name = serializers.SerializerMethodField()
    room_number = serializers.ReadOnlyField(source='room.number')

    class Meta:
        model = Accomodattion
        fields = ['id', 'in_date', 'out_date', 'room_number', 'client_id', 'client_name']

    def get_client_name(self, obj):
        c = obj.client
        if c is None:
            return None
        return c.first_name or c.username

class ProvisionSerializer (serializers. ModelSerializer):
    service = serializers.PrimaryKeyRelatedField(
        queryset=Service.objects.all(), style={'base_template': 'input.html'})
    accomodattion = serializers.PrimaryKeyRelatedField(
        queryset=Accomodattion.objects.all(), style={'base_template': 'input.html'})
    employee = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.select_related('profile'),
        style={'base_template': 'input.html'}, required=False, allow_null=True)
    user_name = serializers.CharField(source='user.username', read_only=True, allow_null=True)
    user_first_name = serializers.CharField(source='user.first_name', read_only=True, allow_null=True)
    accomodattion_info = AccomodattionShortSerializer(source='accomodattion', read_only=True)
    
    class Meta:
        model = Provision
        fields = ['id', 'quantity', 'price', 'service', 'employee', 'accomodattion','accomodattion_info', 'user_name', 'user_first_name']
        read_only_fields = ['price']

    def create(self, validated_data):
        if 'request' in self.context:
            validated_data['user'] = self.context['request'].user
        return ServiceProvision.create_provision(validated_data)

    def update(self, instance, validated_data):
        return ServiceProvision.update_provision(instance, validated_data)

class AccomodattionSerializer (serializers. ModelSerializer):
    room = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all(), style={'base_template': 'input.html'})
    room_number = serializers.CharField(source='room.number', read_only=True, allow_null=True)
    client = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.select_related('profile'),
        style={'base_template': 'input.html'})
    client_name = serializers.CharField(source='client.first_name', read_only=True, allow_null=True)
    client_user = serializers.CharField(source='client.username', read_only=True, allow_null=True)
    user_name = serializers.CharField(source='user.username', read_only=True, allow_null=True)
    user_first_name = serializers.CharField(source='user.first_name', read_only=True, allow_null=True)
    
    class Meta:
        model = Accomodattion
        fields = ['id', 'in_date', 'out_date', 'room','room_number', 'price', 'client','client_name', 'client_user', 'user_name', 'user_first_name']
        read_only_fields = ['price']

    def create(self, validated_data):
        if 'request' in self.context:
            validated_data['user'] = self.context['request'].user
        return ServiceAccomodation.create_accomodattiom(validated_data)

    def update(self, instance, validated_data):
        return ServiceAccomodation.update_accomodattiom(instance, validated_data)

class UserSerializer (serializers. ModelSerializer):
    role = serializers.IntegerField(source='profile.role', read_only=True)
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'role']