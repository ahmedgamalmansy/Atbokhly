from django.db import models
from meal.models import Meal
from django.contrib.auth.models import User
from datetime import datetime 


class Transactions(models.Model):
    user            = models.ForeignKey(User,on_delete=models.CASCADE,null=False,blank=False)
    search_context  = models.CharField(max_length=250,null=False,blank=False)
    result          = models.ManyToManyField(Meal,null=True)
    time            = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)