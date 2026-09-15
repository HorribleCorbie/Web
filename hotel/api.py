from rest_framework import mixins

from rest_framework.viewsets import GenericViewSet

from hotel.models import *
from hotel.serializers import *

class RoomsViewset(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset= Room.objects.all()
    serializer_class = RoomSerializer 

class ServicesViewset(mixins.ListModelMixin, GenericViewSet):
    queryset= Service.objects.all()
    serializer_class = ServiceSerializer

class AccomodattionViewset(mixins.ListModelMixin, GenericViewSet):
    queryset= Accomodattion.objects.all()
    serializer_class = AccomodattionSerializer