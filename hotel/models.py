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

    class Meta:
        verbose_name="Профиль"
        verbose_name_plural = "Профили"

    def __str__(self):
        return self.user.username if self.user else f"Профиль {self.id}"

@receiver(post_save, sender=User)
def on_user_create(sender, instance, created, *args, **kwargs):
     if created:
        Profile.objects.create(user=instance,)

class Room(models.Model):
    number = models.IntegerField("Номер", unique=True)
    description = models.TextField("Описание")
    price = models.FloatField("Цена")

    class Meta:
        verbose_name="Номер"
        verbose_name_plural = "Номера"

    def __str__(self)->str:
        return str(self.number)

class Image(models.Model):
    room = models.ForeignKey("hotel.Room", on_delete=models.CASCADE, null=True, related_name='picture')
    picture = models.ImageField("Изображение", null=True, upload_to="hotel")

    class Meta:
        verbose_name="Изображение"
        verbose_name_plural = "Изображения"

class Accomodattion(models.Model):
    in_date  = models.DateField("Дата въезда")
    out_date = models.DateField("Дата выезда")
    price = models.FloatField("Сумма за проживание", blank=True)

    room = models.ForeignKey("hotel.Room", on_delete=models.CASCADE, null=True)
    client = models.ForeignKey("auth.User", verbose_name="Клиент", on_delete=models.CASCADE, null=True, related_name="client_user")
    
    user = models.ForeignKey("auth.User", verbose_name="Автор записи", on_delete=models.CASCADE, null=True, related_name="author_user")
    
    class Meta:
            verbose_name="Проживание"
            verbose_name_plural = "Проживания"

    def __str__(self)->str:
            outputStr = "С " + str(self.in_date) + " до "+ str(self.out_date) +" " + str(self.client)
            return outputStr
        
    def save(self, *args, **kwargs):
        if not self.price:
            self.price = ((self.out_date-self.in_date).days+1)*self.room.price
        
        super().save(*args, **kwargs)


class Provision(models.Model):
    quantity = models.IntegerField("Количество")
    price = models.FloatField("Сумма", blank=True)
    service = models.ForeignKey("hotel.Service", on_delete=models.CASCADE, null=True)
    employee = models.ForeignKey("auth.User", on_delete=models.CASCADE, null=True, related_name="employee_user_provision")
    accomodattion = models.ForeignKey("hotel.Accomodattion", on_delete=models.CASCADE, null=True)
    
    user = models.ForeignKey("auth.User", verbose_name="Автор записи", on_delete=models.CASCADE, null=True, related_name="author_user_provision")
    
    class Meta:
        verbose_name="Оказание услуги"
        verbose_name_plural = "Оказанные услуги"
        
    def save(self, *args, **kwargs):
        if not self.price:
            self.price = self.quantity*self.service.price
        
        super().save(*args, **kwargs)

class Service(models.Model):
    name = models.TextField("Название")
    price = models.FloatField("Цена")
    picture = models.ImageField("Изображение", null=True, upload_to="hotel")

    class Meta:
        verbose_name="Услуга"
        verbose_name_plural = "Услуги"

    def __str__(self)->str:
        return self.name