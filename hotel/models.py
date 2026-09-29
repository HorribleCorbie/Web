from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    class Role(models.IntegerChoices):
        undefined = 0
        employee = 1
        client = 2
    user = models.OneToOneField("auth.User", on_delete=models.CASCADE, null=True, blank=True)
    role = models.IntegerField("Роль", choices=Role, default=Role.undefined)

    def __str__(self):
        return self.user.username if self.user else f"Profile {self.id}"

@receiver(post_save, sender=User)
def on_user_create(sender, instance, created, *args, **kwargs):
     if created:
        Profile.objects.create(user=instance,)

class Room(models.Model):
    number = models.IntegerField("Номер")
    description = models.TextField("Описание")
    price = models.FloatField("Цена")

    picture = models.ImageField("Изображение", null=True, upload_to="hotel")

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
    client = models.ForeignKey("auth.User", on_delete=models.CASCADE, null=True, related_name="client_user")
    employee = models.ForeignKey("auth.User", on_delete=models.CASCADE, null=True, related_name="employee_user")
    class Meta:
            verbose_name="Проживание"
            verbose_name_plural = "Проживания"

    def __str__(self)->str:
            outputStr = "С " + str(self.in_date) + " до "+ str(self.out_date) +" " + str(self.client)
            return outputStr

class Provision(models.Model):
    quantity = models.IntegerField("Количество")
    price = models.FloatField("Сумма")
    service = models.ForeignKey("hotel.Service", on_delete=models.CASCADE, null=True)
    employee = models.ForeignKey("auth.User", on_delete=models.CASCADE, null=True, related_name="employee_user_provision")
    accomodattion = models.ForeignKey("hotel.Accomodattion", on_delete=models.CASCADE, null=True)
    class Meta:
        verbose_name="Оказание услуги"
        verbose_name_plural = "Оказанные услуги"

class Service(models.Model):
    name = models.TextField("Название")
    price = models.FloatField("Цена")
    picture = models.ImageField("Изображение", null=True, upload_to="hotel")

    class Meta:
        verbose_name="Услуга"
        verbose_name_plural = "Услуги"

    def __str__(self)->str:
        return self.name