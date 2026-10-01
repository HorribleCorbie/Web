from rest_framework import mixins
from django.contrib.auth.models import User
from rest_framework.viewsets import GenericViewSet

from hotel.models import *
from hotel.serializers import *

class RoomsViewset(mixins.CreateModelMixin, 
                   mixins.DestroyModelMixin, 
                   mixins.UpdateModelMixin, 
                   mixins.RetrieveModelMixin, 
                   mixins.ListModelMixin, 
                   GenericViewSet):
    queryset= Room.objects.all()
    serializer_class = RoomSerializer 
    
    def perform_create(self, serializer):
        room = serializer.save()
        files = self.request.FILES.getlist('images') 
        for f in files:
            Image.objects.create(room=room, picture=f)

    def perform_update(self, serializer):
        room = serializer.save()
        
        files = self.request.FILES.getlist('images')
        for f in files:
            Image.objects.create(room=room, picture=f)
            
        delete_images = self.request.data.getlist('images_to_delete')
        for d in delete_images:
            image = Image.objects.get(id=d)
            image.delete() 
        

class ImageViewset(mixins.CreateModelMixin, 
                   mixins.DestroyModelMixin, 
                   mixins.UpdateModelMixin, 
                   mixins.RetrieveModelMixin, 
                   mixins.ListModelMixin, 
                   GenericViewSet):
    queryset= Image.objects.all()
    serializer_class = ImageSerializer 

class ServicesViewset(mixins.CreateModelMixin,
                      mixins.DestroyModelMixin, 
                      mixins.UpdateModelMixin, 
                      mixins.RetrieveModelMixin, 
                      mixins.ListModelMixin, 
                      GenericViewSet):
    queryset= Service.objects.all()
    serializer_class = ServiceSerializer

class AccomodattionViewset(mixins.CreateModelMixin, 
                           mixins.DestroyModelMixin, 
                           mixins.UpdateModelMixin, 
                           mixins.RetrieveModelMixin, 
                           mixins.ListModelMixin, 
                           GenericViewSet):
    queryset= Accomodattion.objects.all()
    serializer_class = AccomodattionSerializer

class ProvisionViewset(mixins.CreateModelMixin, 
                       mixins.DestroyModelMixin, 
                       mixins.UpdateModelMixin, 
                       mixins.RetrieveModelMixin, 
                       mixins.ListModelMixin, 
                       GenericViewSet):
    queryset= Provision.objects.all()
    serializer_class = ProvisionSerializer

class UserViewset(mixins.CreateModelMixin, 
                       mixins.DestroyModelMixin, 
                       mixins.UpdateModelMixin, 
                       mixins.RetrieveModelMixin, 
                       mixins.ListModelMixin, 
                       GenericViewSet):
    queryset= User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = User.objects.all()
        role = self.request.query_params.get('role')

        if role:
            queryset = queryset.filter(profile__role=role)

        return queryset