from django.db import models

# Create your models here.
class room(models.Model):
    name = models.TextField("Название")
    description = models.TextField("Описание")