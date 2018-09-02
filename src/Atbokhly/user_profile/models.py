from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
import random
import os
from django.db.models.signals import post_save
from django.utils import timezone
import datetime
from django.utils.timezone import utc
# Create your models here.

def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name,ext = os.path.splitext(base_name)
    return name,ext

def upload_img(instance,filename):
    new_filename = random.randint(1,21452541)
    name,ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename,ext=ext)
    return "students/{final_filename}".format(final_filename=final_filename)

gender_choices = (
    ('ذكر','ذكر'),
    ('انثى','انثى'))

# class ChefRequest(models.Model):
#     user        = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
#     state       = models.NullBooleanField(null=True, blank=True)
#     created_at  = models.DateTimeField()


class ChiefProfile(models.Model):
    user        = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    first_name  = models.CharField(max_length=50, null=False, blank=True)
    last_name   = models.CharField(max_length=50, null=False, blank=True)
    gender      = models.CharField(max_length=50, null=True, blank=True, choices=gender_choices)
    date_birth  = models.DateField(null=True, blank=True)
    alphanumeric= RegexValidator(r'^[0-9]*$', 'Only alphanumeric characters are allowed.')
    phone       = models.CharField(max_length=11,null=True, blank=True,validators=[alphanumeric])
    email       = models.EmailField(max_length=100, null=False, blank=True)
    img         = models.ImageField(upload_to=upload_img, null=True, blank=True)
    cv          = models.FileField(upload_to=upload_img, null=False, blank=False)
    state       = models.NullBooleanField(null=True, blank=True)
    timestamp   = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return self.first_name+"_"+self.last_name


class UserProfile(models.Model):
    user        = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    first_name  = models.CharField(max_length=50, null=True, blank=True)
    last_name   = models.CharField(max_length=50, null=True, blank=True)
    gender      = models.CharField(max_length=50, null=True, blank=True, choices=gender_choices)
    date_birth  = models.DateField(null=True, blank=True)
    alphanumeric= RegexValidator(r'^[0-9]*$', 'Only alphanumeric characters are allowed.')
    phone       = models.CharField(max_length=11,null=True, blank=True,validators=[alphanumeric])
    email       = models.EmailField(max_length=100, null=True, blank=True)
    img         = models.ImageField(upload_to=upload_img, null=True, blank=True)

    def __str__(self):
        return self.first_name+"_"+self.last_name


class Visitors(models.Model):
    number      = models.IntegerField()
    timestamp   = models.DateTimeField(default=timezone.now())