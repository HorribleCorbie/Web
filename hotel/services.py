from rest_framework.exceptions import ValidationError
from .models import Accomodattion, Profile, Provision

def createAccomodattiom(data):
    in_date= data["in_date"]
    out_date= data["out_date"]
    client = data["client"]
    room = data["room"]
    employee = data["employee"]

    if (in_date>out_date):
        raise ValidationError("Дата въезда не может быть больше выезда.")

    if (client.profile.role != Profile.Role.client):
        raise ValidationError("Клиент должен быть зарегестрирован.")

    if (employee.profile.role != Profile.Role.employee):
            raise ValidationError("Сотрудник должен быть зарегестрирован.")

    price = ((out_date-in_date).days+1)*room.price

    existing = Accomodattion.objects.filter(room=room,
                                            in_date__lte=out_date,
                                            out_date__gte=in_date)
    
    if (existing.exists()):
        raise ValidationError("Уже есть бронь на эти даты.")

    return Accomodattion.objects.create(
        room=room,
        client=client,
        employee=employee,
        in_date=in_date,
        out_date=out_date,
        price=price
    )

def updateAccomodattiom(instance, data):
    in_date= data["in_date"]
    out_date= data["out_date"]
    client = data["client"]
    room = data["room"]
    employee = data["employee"]

    if (in_date>out_date):
        raise ValidationError("Дата въезда не может быть больше выезда.")

    if (client.profile.role != Profile.Role.client):
        raise ValidationError("Клиент должен быть зарегестрирован.")

    if (employee.profile.role != Profile.Role.employee):
            raise ValidationError("Сотрудник должен быть зарегестрирован.")

    price = ((out_date-in_date).days+1)*room.price

    existing = Accomodattion.objects.filter(room=room,
                                            in_date__lte=out_date,
                                            out_date__gte=in_date).exclude(id= instance.id)
    
    if (existing.exists()):
        raise ValidationError("Уже есть бронь на эти даты.")

    for attr, value in data.items():
            setattr(instance, attr, value)
    
    instance.price = price

    instance.save()

    return instance

def createProvision(data):
    employee = data["employee"]
    accomodattion = data["accomodattion"]
    service = data["service"]
    quantity = data["quantity"]

    if (employee.profile.role != Profile.Role.employee):
        raise ValidationError("Сотрудник должен быть зарегестрирован.")

    if (quantity<=0 or quantity>100):
         raise ValidationError("Количество должно быть в диапазоне от 1 до 100")


    price = service.price * quantity

    return Provision.objects.create(
        service=service,
        accomodattion=accomodattion,
        employee=employee,
        quantity=quantity,
        price=price
        )

def updateProvision(instance, data):
    employee = data["employee"]
    service = data["service"]
    quantity = data["quantity"]

    if (employee.profile.role != Profile.Role.employee):
        raise ValidationError("Сотрудник должен быть зарегестрирован.")

    if (quantity<=0 or quantity>100):
         raise ValidationError("Количество должно быть в диапазоне от 1 до 100")

    for attr, value in data.items():
        setattr(instance, attr, value)

    price = service.price * quantity
    instance.price = price

    instance.save() 
    
    return instance