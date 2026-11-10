from django.db.models.aggregates import Avg, Count, Max, Min
from django.db.models.functions import Lower
from rest_framework import mixins
from io import BytesIO
from django.http import HttpResponse
import pandas
from django.contrib.auth.models import User
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from rest_framework.viewsets import GenericViewSet
from django.db.models import Q
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
            
        if (num := p.get('number')) and num.isdigit():
            qs = qs.filter(number=num)
        
        if (des := p.get('description')):
            qs = qs.annotate(description_lower=Lower('description')).filter(description_lower__contains=des.lower())
        
        if (price := p.get('price')) and price.isdigit():
            qs = qs.filter(price__lte=price).order_by('price')
        
        
        return qs
    
    
    @action(detail=False, url_path="authors", methods=['get'])
    def authors(self, request):
        qs = (User.objects
            .filter(author_user_room__isnull=False)
            .values('id', 'username', 'first_name')
            .distinct()
            .order_by('username'))
        return Response(list(qs))
    
    @action(detail=False, url_path="export", methods=['get'])
    def import_to_excel(self, request):
        objs = Room.objects.all()
        data = []
        for obj in objs:
            data.append({
                "id": obj.id,
                "number": obj.number,
                "price": obj.price,
                "description": obj.description,
                "user_nickname": obj.user,
                "user_first_name": obj.user_first_name
            })
            
        df = pandas.DataFrame(data=data, columns=['id', 'number', 'price', 'description'])
        output = BytesIO()
        writer = pandas.ExcelWriter(output,engine='xlsxwriter')
        df.to_excel(writer, index=False)
        
        output.seek(0)
        writer.close()
        
        response = HttpResponse(
            output.getvalue(), 
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=Report.xlsx'

        return response
    
    class StatsSerializer (serializers.Serializer):
        count = serializers. IntegerField()
        avg = serializers.FloatField()
        max = serializers. IntegerField()
        min = serializers. IntegerField()
    
    
    @action(detail=False, methods=["GET"], url_path="stats")
    def get_stats (self, request, *args,**kwargs):
        stats = Room.objects.aggregate(
            count=Count("*"),
            avg=Avg("price"),
            max=Max("id"),
            min=Min("id"),)
        serializer = self.StatsSerializer (instance=stats)
        return Response (serializer.data)
    
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

    class StatsSerializer (serializers.Serializer):
        count = serializers. IntegerField()
        avg = serializers.FloatField()
        max = serializers. IntegerField()
        min = serializers. IntegerField()
    
    @action(detail=False, url_path="export", methods=['get'])
    def import_to_excel(self, request):
        objs = Service.objects.all()
        data = []
        for obj in objs:
            data.append({
                "id": obj.id,
                "name": obj.name,
                "price": obj.price,
                "user": obj.user,
                "user_id": obj.user_id
            })
            
        df = pandas.DataFrame(data=data, columns=['id', 'name', 'price', 'user', 'user_id'])
        output = BytesIO()
        writer = pandas.ExcelWriter(output,engine='xlsxwriter')
        df.to_excel(writer, index=False)
        
        output.seek(0)
        writer.close()
        
        response = HttpResponse(
            output.getvalue(), 
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=Report.xlsx'

        return response
    
    @action(detail=False, methods=["GET"], url_path="stats")
    def get_stats (self, request, *args,**kwargs):
        stats = Service.objects.aggregate(
            count=Count("*"),
            avg=Avg("price"),
            max=Max("id"),
            min=Min("id"),)
        serializer = self.StatsSerializer (instance=stats)
        return Response (serializer.data)
    
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
            
        if (name := p.get('name')):
            qs = qs.annotate(name_lower=Lower('name')).filter(name_lower__contains=name.lower())
                
        if (price := p.get('price')) and price.isdigit():
            qs = qs.filter(price__lte=price).order_by('price')
        
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
    
    @action(detail=False, url_path="export", methods=['get'])
    def import_to_excel(self, request):
        objs = Accomodattion.objects.all()
        data = []
        for obj in objs:
            data.append({
                "id": obj.id,
                "in_date": obj.in_date,
                "out_date": obj.out_date,
                "room": obj.room,
                "client": obj.client,
                "user_name": obj.user,
            })
        
            
        df = pandas.DataFrame(data=data, columns=['id', 'in_date', 'out_date', 
                                                  'room', 'client', 'user_name'])
        output = BytesIO()
        writer = pandas.ExcelWriter(output,engine='xlsxwriter')
        df.to_excel(writer, index=False)
        
        output.seek(0)
        writer.close()
        
        response = HttpResponse(
            output.getvalue(), 
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=Report.xlsx'

        return response
    
    class StatsSerializer (serializers.Serializer):
        count = serializers. IntegerField()
        avg = serializers.FloatField()
        max = serializers. IntegerField()
        min = serializers. IntegerField()
    
    @action(detail=False, methods=["GET"], url_path="stats")
    def get_stats (self, request, *args,**kwargs):
        stats = Accomodattion.objects.aggregate(
            count=Count("*"),
            avg=Avg("price"),
            max=Max("id"),
            min=Min("id"),)
        serializer = self.StatsSerializer (instance=stats)
        return Response (serializer.data)
    
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
        user = self.request.user

        if not user.is_superuser:
            role = user.profile.role

            if role == Profile.Role.client:
                qs = qs.filter(client=user)
            else:
                qs = qs.filter(user=user)

        if (author := p.get('user')) and author.isdigit():
            if user.is_superuser:
                qs = qs.filter(user_id=author)

        if p.get('actual') == '1':
            today = timezone.localdate()
            qs = qs.filter(
                in_date__lte=today,
                out_date__gte=today
            )

        if (num := p.get('number')) and num.isdigit():
            qs = qs.filter(room__number=num)

        if (date := p.get('in_date')):
            qs = qs.filter(in_date__gte=date)

        if (date := p.get('out_date')):
            qs = qs.filter(out_date__lte=date)

        if (price := p.get('price')) and price.isdigit():
            qs = qs.filter(price__lte=price)

        if (client := p.get('client')):
            qs = qs.annotate(
                    first_name_lower=Lower('client__first_name'),
                    username_lower=Lower('client__username')
                ).filter(
                    Q(first_name_lower__contains=client.lower()) |
                    Q(first_name_lower='') & Q(username_lower__contains=client.lower())
                )

        return qs
        
        

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
    
    @action(detail=False, url_path="export", methods=['get'])
    def import_to_excel(self, request):
        objs = Provision.objects.all()
        data = []
        for obj in objs:
            data.append({
                "id": obj.id,
                "quantity": obj.quantity,
                "service": obj.service,
                "employee": obj.employee,
                "accomodattion": obj.accomodattion,
                "user": obj.user,
            })
        
            
        df = pandas.DataFrame(data=data, columns=['id', 'quantity', 'service', 
                                                  'employee', 'accomodattion', 'user'])
        output = BytesIO()
        writer = pandas.ExcelWriter(output,engine='xlsxwriter')
        df.to_excel(writer, index=False)
        
        output.seek(0)
        writer.close()
        
        response = HttpResponse(
            output.getvalue(), 
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=Report.xlsx'

        return response
    
    class StatsSerializer (serializers.Serializer):
        count = serializers. IntegerField()
        avg = serializers.FloatField()
        max = serializers. IntegerField()
        min = serializers. IntegerField()
    
    @action(detail=False, methods=["GET"], url_path="stats")
    def get_stats (self, request, *args,**kwargs):
        stats = Provision.objects.aggregate(
            count=Count("*"),
            avg=Avg("id"),
            max=Max("id"),
            min=Min("id"),)
        serializer = self.StatsSerializer (instance=stats)
        return Response (serializer.data)
        
    
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
        user = self.request.user

        if not user.is_superuser:
            role = user.profile.role

            if role == Profile.Role.client:
                qs = qs.filter(accomodattion__client=user)
            else:
                qs = qs.filter(user=user)

        if (author := p.get('user')) and author.isdigit():
            if user.is_superuser:
                qs = qs.filter(user_id=author)

        if (service := p.get('service')):
                qs = qs.annotate(
                service__name_lower=Lower('service__name')
            ).filter(service__name_lower__icontains=service)

        if (quantity := p.get('quantity')) and quantity.isdigit():
            qs = qs.filter(quantity=quantity)

        if (price := p.get('price')) and price.isdigit():
            qs = qs.filter(price__lte=price)

        if (num := p.get('number')) and num.isdigit():
            qs = qs.filter(accomodattion__room__number=num)

        if (date := p.get('in_date')):
            qs = qs.filter(accomodattion__in_date__gte=date)

        if (date := p.get('out_date')):
            qs = qs.filter(accomodattion__out_date__lte=date)

        if (client := p.get('client')):
            qs = qs.annotate(
                client_first_name_lower=Lower('accomodattion__client__first_name'),
                client_username_lower=Lower('accomodattion__client__username')
            ).filter(
                Q(client_first_name_lower__contains=client.lower()) |
                (
                    Q(accomodattion__client__first_name__isnull=True) |
                    Q(accomodattion__client__first_name='')
                ) &
                Q(client_username_lower__contains=client.lower())
            )

        return qs


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
        
        if(role==Profile.Role.client):
            return queryset.filter(username=self.request.user.get_username)

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