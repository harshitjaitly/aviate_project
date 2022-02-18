from django.db import models
from .soft_delete import ParanoidModel
# Create your models here.

import os


def path_and_rename(instance, filename):
    upload_to = 'media'
    ext = filename.split('.')[-1]

    instance.count = instance.count+1
    print(instance.count)
    filename = '{}_{}.{}'.format(instance.name,instance.count, ext)
    return os.path.join(upload_to, filename)

class Profile(ParanoidModel) :

    name = models.CharField(max_length=255)
    age = models.IntegerField()
    contact = models.IntegerField()
    count = models.IntegerField(editable=False, default=0)


    resume = models.FileField(upload_to=path_and_rename, max_length=255, null=True, blank=True, default=None)
    resume_list = models.JSONField(editable=False, default=dict)


    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)


    def __str__(self) :
        return self.name
