from django.db import models
from .soft_delete import CustomModel
import os


# Create your models here.

"""
Custom-Function which renames the uploaded Resume Files
FileName format : <Profile_Name>_<Resume_Number>
"""
def path_and_rename(instance, filename):
    upload_to = 'media'
    ext = filename.split('.')[-1]

    print(instance.count)
    filename = '{}_{}.{}'.format(instance.name,instance.count, ext)
    return os.path.join(upload_to, filename)

"""
Description Of Profile Model Field

Required Fields : Name, Password, Age, Contact
Non-Editable Fields : count (stores the count of resumes uploaded) , prev_resume_list (stores the directory address of OLD Resumes)
"""
class Profile(CustomModel) :

    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255, blank=False)
    age = models.IntegerField()
    contact = models.IntegerField()

    resume = models.FileField(upload_to=path_and_rename, max_length=255, null=True, blank=True, default=None)

    count = models.IntegerField(editable=False, default=1)
    prev_resume_list = models.JSONField(editable=False, default=dict)

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

    def __str__(self) :
        return self.name
