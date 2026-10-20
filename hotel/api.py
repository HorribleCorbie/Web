from rest_framework import mixins
from django.contrib.auth.models import User
from rest_framework.decorators import action
from rest_framework.response import Response

from rest_framework.viewsets import GenericViewSet
from django.contrib.auth import logout as django_logout
from django.contrib.auth import login as django_login
from django.contrib.auth import authenticate

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
    
    def get_queryset(self):
        if self.request.user.is_superuser:
            qs = super().get_queryset()
            return qs
        else:
            qs = super().get_queryset()
            
            qs = qs.filter(user=self.request.user)

            return qs

class ProvisionViewset(mixins.CreateModelMixin, 
                       mixins.DestroyModelMixin, 
                       mixins.UpdateModelMixin, 
                       mixins.RetrieveModelMixin, 
                       mixins.ListModelMixin, 
                       GenericViewSet):
    queryset= Provision.objects.all()
    serializer_class = ProvisionSerializer
    
    def get_queryset(self):
        if self.request.user.is_superuser:
            qs = super().get_queryset()
            return qs
        else:
            qs = super().get_queryset()
            
            qs = qs.filter(user=self.request.user)

            return qs

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
    
class ProfileViewSet(GenericViewSet):
    queryset = User.objects.all()

    @action(detail=False, url_path="me", methods=['GET'])
    def get_me(self, request, *args, **kwargs):
        data = {
            'is_authenticated': self.request.user.is_authenticated,
            'is_superuser': self.request.user.is_superuser
        }

        if self.request.user.is_authenticated:
            data.update({
                "username": self.request.user.username,
                "id": self.request.user.id,
                "role": self.request.user.profile.role,
            })

        return Response(data=data)

    @action(detail=False, url_path="logout", methods=['POST'])
    def logout(self, *args, **kwargs):
        django_logout(self.request)

        return Response()

    @action(detail=False, url_path="login", methods=['POST'])
    def login(self, *args, **kwargs):
        username = self.request.data['username']
        password = self.request.data['password']

        success = False
        status_code = 403
        
        user = authenticate(username=username, password=password)
        if user:
            success = True
            status_code = 200
            django_login(self.request, user)

        return Response({
            'success': success
        }, status=status_code)

    @action(detail=False, url_path="register", methods=['POST'])
    def register(self, *args, **kwargs):
        username = self.request.data['username']
        password = self.request.data['password']
        
        success = False
        status_code = 403
        
        if User.objects.filter(username=username).exists():
            return  Response({
            'success': False, "error": "Такой никнейм уже занят"
        }, status=status_code)
        
        user = User.objects.create_user(
            username=username,
            password=password
        )
        
        if user:
            success = True
            status_code = 200
            django_login(self.request, user)

        return Response({
            'success': success
        }, status=status_code)
        

    # @action(detail=False, url_path="activate_user", methods=['POST'])
    # def activate_user(self, *args, **kwargs):
    #     pass