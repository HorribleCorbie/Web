from rest_framework import mixins
from django.contrib.auth.models import User
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
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
    queryset = Room.objects.select_related('user').prefetch_related('picture').order_by('number')
    serializer_class = RoomSerializer 
    
    def get_queryset(self):
        qs =super().get_queryset()
        p = self.request.query_params
        
        if (author := p.get('user')) and author.isdigit():
            qs = qs.filter(user_id=author)
        
        return qs
    
    @action(detail=False, url_path="authors", methods=['get'])
    def authors(self, request):
        qs = (User.objects
            .filter(author_user_room__isnull=False)
            .values('id', 'username', 'first_name')
            .distinct()
            .order_by('username'))
        return Response(list(qs))
    
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
    queryset= Service.objects.select_related('user')
    serializer_class = ServiceSerializer
    
    @action(detail=False, url_path="authors", methods=['get'])
    def authors(self, request):
        qs = (User.objects
            .filter(author_user_service__isnull=False)
            .values('id', 'username', 'first_name')
            .distinct()
            .order_by('username'))
        return Response(list(qs))
    
    def get_queryset(self):
        qs =super().get_queryset()
        p = self.request.query_params
        
        if (author := p.get('user')) and author.isdigit():
            qs = qs.filter(user_id=author)
        
        return qs

class AccomodattionViewset(mixins.CreateModelMixin, 
                           mixins.DestroyModelMixin, 
                           mixins.UpdateModelMixin, 
                           mixins.RetrieveModelMixin, 
                           mixins.ListModelMixin, 
                           GenericViewSet):
    queryset= Accomodattion.objects.select_related(
        'room',
        'client',
        'user'
    )
    serializer_class = AccomodattionSerializer
    
    @action(detail=False, url_path="authors", methods=['get'])
    def authors(self, request):
        qs = (User.objects
            .filter(author_user__isnull=False)
            .values('id', 'username', 'first_name')
            .distinct()
            .order_by('username'))
        return Response(list(qs))
    
    def get_queryset(self):
        qs = super().get_queryset()
        
        p = self.request.query_params
        
        if (author := p.get('user')) and author.isdigit():
            qs = qs.filter(user_id=author)
            
        if p.get('actual') == '1':
            today = timezone.localdate()
            qs = qs.filter(
                in_date__lte=today,
                out_date__gte=today
            )
        
        if self.request.user.is_superuser:
            return qs
        
        role = self.request.user.profile.role
        if(role==Profile.Role.client):
            return qs.filter(client=self.request.user)
        
        return qs.filter(user=self.request.user)
        

class ProvisionViewset(mixins.CreateModelMixin, 
                       mixins.DestroyModelMixin, 
                       mixins.UpdateModelMixin, 
                       mixins.RetrieveModelMixin, 
                       mixins.ListModelMixin, 
                       GenericViewSet):
    queryset= Provision.objects.select_related(
        'accomodattion__client',
        'accomodattion__room',
        'service',
        'employee',
        'user'
    )
    serializer_class = ProvisionSerializer
    
    @action(detail=False, url_path="authors", methods=['get'])
    def authors(self, request):
        qs = (User.objects
            .filter(author_user_provision__isnull=False)
            .values('id', 'username', 'first_name')
            .distinct()
            .order_by('username'))
        return Response(list(qs))
    
    def get_queryset(self):
        qs = super().get_queryset()
        
        p = self.request.query_params
                
        if (author := p.get('user')) and author.isdigit():
            qs = qs.filter(user_id=author)
        
        if self.request.user.is_superuser:
            return qs
        
        role = self.request.user.profile.role
        if(role==Profile.Role.client):
            return qs.filter(accomodattion__client=self.request.user)
        
        return qs.filter(user=self.request.user)


class UserViewset(mixins.CreateModelMixin, 
                       mixins.DestroyModelMixin, 
                       mixins.UpdateModelMixin, 
                       mixins.RetrieveModelMixin, 
                       mixins.ListModelMixin, 
                       GenericViewSet):
    queryset= User.objects.select_related('profile')
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
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