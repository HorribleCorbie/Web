from django.db import models

# Create your models here.
class Room(models.Model):
    number = models.IntegerField("Номер")
    description = models.TextField("Описание")
    price = models.FloatField("Цена")

    class Meta:
        verbose_name="Номер"
        verbose_name_plural = "Номера"

    def __str__(self)->str:
        return str(self.number)

class Accomodattion(models.Model):
    in_date  = models.DateField("Дата въезда")
    out_date = models.DateField("Дата выезда")
    price = models.FloatField("Сумма за проживание")

    room = models.ForeignKey("hotel.Room", on_delete=models.CASCADE, null=True)
    # client = models.ForeignKey("auth.User", on_delete=models.CASCADE, null=True, related_name="client_user")
    # employee = models.ForeignKey("auth.User", on_delete=models.CASCADE, null=True, related_name="employee_user")
    class Meta:
            verbose_name="Проживание"
            verbose_name_plural = "Проживаний"

class Provision(models.Model):
    quantity = models.IntegerField("Количество")
    price = models.FloatField("Сумма")
    # service = models.ForeignKey("hotel.Service", on_delete=models.CASCADE, null=True)
    # client = models.ForeignKey("auth.User", on_delete=models.CASCADE, null=True, related_name="client_user")
    # employee = models.ForeignKey("auth.User", on_delete=models.CASCADE, null=True, related_name="employee_user")
    # accomodattion = models.ForeignKey("auth.Accomodattion", on_delete=models.CASCADE, null=True)

class Service(models.Model):
    name = models.TextField("Название")
    price = models.FloatField("Цена")
