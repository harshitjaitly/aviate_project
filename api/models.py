from django.db import models
from .soft_delete import ParanoidModel
# Create your models here.

class Profile(ParanoidModel) :

    name = models.CharField(max_length=255)
    age = models.IntegerField()
    contact = models.IntegerField()
    resume = models.CharField(max_length=255)

    def __str__(self) :
        return self.name
