from django.test import TestCase
from rest_framework.test import APIClient
from model_bakery import baker

from hotel.models import *

class RoomViewsetTestCase (TestCase):
    def test_get_list_rooms(self):
        rooms = baker.make("hotel.Room")

        r = self.client.get('/api/rooms/')
        data = r.json()
        print(data)

        assert rooms.number == data[0]['number']
        assert rooms.description == data[0]['description']
        assert rooms.price == data[0]['price']
        assert len(data) == 1

    def test_create_room(self):
        r = self.client.post("/api/rooms/", {
            "number": 2,
            "description": "Второй номер",
            "price": 200
        })
        new_room_id = r.json()['id']

        rooms = Room.objects.all()
        assert len(rooms) == 1

        new_room = Room.objects.filter(id=new_room_id).first()
        assert new_room.number == 2
        assert new_room.description == "Второй номер"
        assert new_room.price == 200

    def test_delete_room(self):
        rooms = baker.make("Room", 10)
        r = self.client.get('/api/rooms/')
                            
        data = r.json()
        assert len(data) == 10

        
        rooms_id_to_delete = rooms[3].id
        self.client.delete(f'/api/rooms/{rooms_id_to_delete}/')
        r = self.client.get('/api/rooms/')
        data = r.json()
        assert len(data) == 9

        assert rooms_id_to_delete not in [i['id'] for i in data]

    def test_update_room(self):
        rooms = baker.make("Room", 10)
        room: Room = rooms[2]

        r = self.client.get(f'/api/rooms/{room.id}/')
        data = r.json()
        assert data['number'] == room.number

        self.client = APIClient()

        r = self.client.put(f'/api/rooms/{room.id}/', {
            "number": 100,
            "description": room.description,
            "price": room.price,
        }, format='json')
        assert r.status_code == 200

        r = self.client.get(f'/api/rooms/{room.id}/')
        data = r.json()

        assert data['number'] == 100
        room.refresh_from_db()
        assert data['number'] == room.number

class AccomodattionViewsetTestCase (TestCase):
    def test_get_list_accomodattion(self):
        
        client = baker.make("auth.User")
        employee = baker.make("auth.User")
        room = baker.make("hotel.Room")
        accomodattion = baker.make("hotel.Accomodattion", room=room, employee=employee, client=client)

        r = self.client.get('/api/accomodattion/')
        data = r.json()
        print(data)

        
        assert str(accomodattion.in_date) == data[0]['in_date']
        assert str(accomodattion.out_date) == data[0]['out_date']
        assert accomodattion.price == data[0]['price']

        assert accomodattion.client.id == data[0]['client']
        assert accomodattion.employee.id == data[0]['employee']
        assert accomodattion.room.id == data[0]['room']

        assert len(data) == 1
     
    def test_create_accomodattion(self):
        client = baker.make("auth.User")
        employee = baker.make("auth.User")
        room = baker.make("hotel.Room")

        r = self.client.post("/api/accomodattion/", {
            "client": client.id,
            "employee": employee.id,
            "room": room.id,
            "in_date": "2026-09-15",
            "out_date": "2026-09-20",
            "price": 3000
        })
        new_accomodattion_id = r.json()['id']

        accomodattions = Accomodattion.objects.all()
        assert len(accomodattions) == 1

        new_accomodattion = Accomodattion.objects.filter(id=new_accomodattion_id).first()
        assert new_accomodattion.client.id == client.id
        assert new_accomodattion.employee.id == employee.id
        assert new_accomodattion.room.id == room.id
        assert str(new_accomodattion.in_date) == "2026-09-15"
        assert str(new_accomodattion.out_date) == "2026-09-20"
        assert new_accomodattion.price == 3000

    def test_update_accomodattion(self):
        accomodattions = [
            baker.make(
                "hotel.Accomodattion",
                client=baker.make("auth.User"),
                employee=baker.make("auth.User"),
                room=baker.make("hotel.Room"),
            )
            for _ in range(10)
        ]
        accomodattion: Accomodattion = accomodattions[2]

        r = self.client.get(f'/api/accomodattion/{accomodattion.id}/')
        data = r.json()
        assert data['price'] == accomodattion.price

        self.client = APIClient()

        r = self.client.put(f'/api/accomodattion/{accomodattion.id}/', {
            "client": accomodattion.client.id,
            "employee": accomodattion.employee.id,
            "room": accomodattion.room.id,
            "in_date": str(accomodattion.in_date),
            "out_date": str(accomodattion.out_date),
            "price": 9999,
        }, format='json')
        assert r.status_code == 200

        r = self.client.get(f'/api/accomodattion/{accomodattion.id}/')
        data = r.json()

        assert data['price'] == 9999
        accomodattion.refresh_from_db()
        assert data['price'] == accomodattion.price

    def test_delete_accomodattion(self):
        accomodattions = baker.make("hotel.Accomodattion", 10)
        r = self.client.get('/api/accomodattion/')
        data = r.json()
        assert len(data) == 10

        accomodattions_id_to_delete = accomodattions[3].id
        self.client.delete(f'/api/accomodattion/{accomodattions_id_to_delete}/')
        r = self.client.get('/api/accomodattion/')
        data = r.json()
        assert len(data) == 9

        assert accomodattions_id_to_delete not in [i['id'] for i in data]

class ProvisionViewsetTestCase (TestCase):
    def test_get_list_provision(self):
        service = baker.make("hotel.Service")
        accomodattion = baker.make("hotel.Accomodattion")
        employee = baker.make("auth.User")

        provision = baker.make("hotel.Provision", service=service, accomodattion=accomodattion, employee=employee)

        r = self.client.get('/api/provision/')
        data = r.json()
        print(data)

        assert provision.quantity == data[0]['quantity']
        assert provision.price == data[0]['price']
        assert provision.service.id == data[0]['service']
        assert provision.accomodattion.id == data[0]['accomodattion']
        assert provision.employee.id == data[0]['employee']
        
        assert len(data) == 1

    def test_create_provision(self):

        service = baker.make("hotel.Service")
        accomodattion = baker.make("hotel.Accomodattion")
        employee = baker.make("auth.User")

        r = self.client.post("/api/provision/", {
            "service": service.id,
            "accomodattion": accomodattion.id,
            "employee": employee.id,
            "quantity": 3,
            "price": 1500
        })
        new_provision_id = r.json()['id']

        provisions = Provision.objects.all()
        assert len(provisions) == 1

        new_provision = Provision.objects.filter(id=new_provision_id).first()
        assert new_provision.service.id == service.id
        assert new_provision.accomodattion.id == accomodattion.id
        assert new_provision.employee.id == employee.id
        assert new_provision.quantity == 3
        assert new_provision.price == 1500

    def test_update_provision(self):
            provisions = [
                baker.make(
                    "hotel.Provision",
                    service=baker.make("hotel.Service"),
                    accomodattion=baker.make("hotel.Accomodattion"),
                    employee=baker.make("auth.User"),
                )
                for _ in range(10)
            ]
            provision: Provision = provisions[2]
    
            r = self.client.get(f'/api/provision/{provision.id}/')
            data = r.json()
            assert data['quantity'] == provision.quantity
    
            self.client = APIClient()
    
            r = self.client.put(f'/api/provision/{provision.id}/', {
                "service": provision.service.id,
                "accomodattion": provision.accomodattion.id,
                "employee": provision.employee.id,
                "quantity": 100,
                "price": provision.price,
            }, format='json')
            assert r.status_code == 200
    
            r = self.client.get(f'/api/provision/{provision.id}/')
            data = r.json()
    
            assert data['quantity'] == 100
            provision.refresh_from_db()
            assert data['quantity'] == provision.quantity

    def test_delete_provision(self):
        provisions = baker.make("hotel.Provision", 10)
        r = self.client.get('/api/provision/')
        data = r.json()
        assert len(data) == 10

        provisions_id_to_delete = provisions[3].id
        self.client.delete(f'/api/provision/{provisions_id_to_delete}/')
        r = self.client.get('/api/provision/')
        data = r.json()
        assert len(data) == 9

        assert provisions_id_to_delete not in [i['id'] for i in data]
    

class ServiceViewsetTestCase (TestCase):
    def test_get_list_services(self):
        services = baker.make("hotel.Service")

        r = self.client.get('/api/service/')
        data = r.json()
        print(data)

        assert services.id == data[0]['id']
        assert services.name == data[0]['name']
        assert services.price == data[0]['price']
        assert len(data) == 1


    def test_create_service(self):

        r = self.client.post("/api/service/", {
            "name": "Уборка",
            "price": 500
        })
        new_service_id = r.json()['id']

        services = Service.objects.all()
        assert len(services) == 1

        new_service = Service.objects.filter(id=new_service_id).first()
        assert new_service.name == "Уборка"
        assert new_service.price == 500


    def test_delete_service(self):
        services = baker.make("hotel.Service", 10)
        r = self.client.get('/api/service/')
        data = r.json()
        assert len(data) == 10

        services_id_to_delete = services[3].id
        self.client.delete(f'/api/service/{services_id_to_delete}/')
        r = self.client.get('/api/service/')
        data = r.json()
        assert len(data) == 9

        assert services_id_to_delete not in [i['id'] for i in data]


    def test_update_service(self):
        services = baker.make("hotel.Service", 10)
        service: Service = services[2]

        r = self.client.get(f'/api/service/{service.id}/')
        data = r.json()
        assert data['name'] == service.name

        self.client = APIClient()

        r = self.client.put(f'/api/service/{service.id}/', {
            "name": "Новое название",
            "price": service.price,
        }, format='json')
        assert r.status_code == 200

        r = self.client.get(f'/api/service/{service.id}/')
        data = r.json()

        assert data['name'] == "Новое название"
        service.refresh_from_db()
        assert data['name'] == service.name