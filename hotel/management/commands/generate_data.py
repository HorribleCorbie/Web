import requests
import random
from datetime import timedelta
from django.utils import timezone
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from faker import Faker

from hotel.models import *


class Command(BaseCommand):
    def handle(self, *args, **options):
        fake = Faker(['ru_RU'])
        
        today = timezone.localdate()
        
        user = User.objects.filter(is_superuser=True).first()
        clients = list(User.objects.filter(
            profile__role=Profile.Role.client
        ))

        employees = list(User.objects.filter(
            profile__role=Profile.Role.employee
        ))
        
        services = list(Service.objects.all())
        
        accommodattions = list(Accomodattion.objects.filter(in_date__lt=today,
                                                            out_date__gt=today))
        
        numbers= [i.room.number for i in accommodattions]
        
        rooms = list(Room.objects.exclude(number__in=numbers))
        i=147
        
        for j in range(len(rooms)):
            # response = requests.get("https://picsum.photos/400/300")
            # Room.objects.create(
            #     number = i+j,
            #     description=fake.text(max_nb_chars=200),
            #     price=float(fake.random_int(min=100, max=500)),
            #     user = user)
            
            # Service.objects.create(
            #     name=fake.word().capitalize(),
            #     price=float(fake.random_int(min=10, max=100)),
            #     picture=ContentFile(
            #         response.content,
            #         name=f"service_{i}.jpg"
            #     ),
            #     user=user
            # )
            
            user = User.objects.create_user(
                username=fake.unique.user_name(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.email(),
                password="123"
            )
            
            user.profile.role = Profile.Role.client
            
            user.profile.save()
            
            # client = random.choice(clients)
            # clients.remove(client)
            
            employee = random.choice(employees)
            employees.remove(employee)
            
            room = random.choice(rooms)
            rooms.remove(room)
            
            start_date = today - timedelta(
                days=random.randint(1, 14)
            )

            end_date = today + timedelta(
                days=random.randint(1, 60)
            )
            
            accommodattion = Accomodattion.objects.create(
                in_date  = start_date,
                out_date = end_date,
            
                room = room,
                client = user,
                
                user = employee
            )
            
            service=random.choice(services)
            
            
            Provision.objects.create(
                quantity = fake.random_int(min=1, max=5),
                service = service,
                employee = employee,
                accomodattion = accommodattion,
                
                user = employee
            )
            