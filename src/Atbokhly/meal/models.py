from django.db import models
from django.db.models.signals import pre_save, post_save
from search.utils import unique_slug_generator
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator,MaxValueValidator
import random
import os
from django.core.exceptions import ValidationError

# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.category_name


class Ingredient(models.Model):
    ingredient_name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.ingredient_name


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    print(base_name)
    name,ext = os.path.splitext(base_name)
    return name,ext

def upload_img(instance,filename):
    print(filename)
    name,ext = get_filename_ext(filename)
    new_filename = name + str(random.randint(1, 21452541))
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename,ext=ext)
    return "meals/{final_filename}".format(final_filename=final_filename)

def upload_video(instance,filename):
    print(filename)
    name,ext = get_filename_ext(filename)
    new_filename = name + str(random.randint(1, 21452541))
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename,ext=ext)
    return "meals/{final_filename}".format(final_filename=final_filename)


class Meal(models.Model):
    meal_owner      = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    meal_name       = models.CharField(max_length=150, unique=False)
    meal_recipe     = models.TextField()
    meal_category   = models.ForeignKey(Category, on_delete=models.CASCADE)
    ingredients     = models.ManyToManyField(Ingredient)
    img             = models.ImageField(upload_to=upload_img, null=False, blank=False)
    video           = models.FileField(upload_to=upload_video, null=True, blank=True)
    slug            = models.SlugField(null=True, blank=True)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.meal_name

    @property
    def title(self):
        return self.meal_name



def meal_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(meal_pre_save_receiver, sender=Meal)


class Feedback(models.Model):
    meal_id     = models.ForeignKey(Meal, on_delete=models.CASCADE)
    name        = models.CharField(max_length=100,null=True)
    user_mail   = models.CharField(max_length=100)
    content     = models.TextField()
    def __str__(self):
        return self.name


class Comment(models.Model):
    meal        = models.ForeignKey(Meal,on_delete=models.CASCADE)
    comment     = models.CharField(max_length=1000)
    user        = models.ForeignKey(User,on_delete=models.CASCADE)
    timeStemp   = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.username+" => "+self.meal.meal_name


class Reply(models.Model):
    # meal        = models.ForeignKey(Meal,on_delete=models.CASCADE)
    reply       = models.CharField(max_length=1000)
    comment     = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user        = models.ForeignKey(User,on_delete=models.CASCADE)
    timeStemp   = models.DateTimeField(auto_now_add=True)



class ReactValues(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)

class LikeComment(models.Model):
    reply    = models.ForeignKey(Reply, on_delete=models.CASCADE, null=True, blank=True)
    comment     = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True)
    user        = models.ForeignKey(User,on_delete=models.CASCADE)
    react_value = models.BooleanField()
    # react_value = models.ForeignKey(ReactValues,on_delete=models.CASCADE)


class Rate(models.Model):
    meal        = models.ForeignKey(Meal,on_delete=models.CASCADE)
    rate_value  = models.FloatField(validators=[MinValueValidator(0),MaxValueValidator(5)])
    Votes       = models.PositiveIntegerField()
    # user    = models.ForeignKey(User,on_delete=models.CASCADE)
    def __str__(self):
        return self.meal.meal_name

class UserRate(models.Model):
    meal        = models.ForeignKey(Meal,on_delete=models.CASCADE)
    rate_value  = models.FloatField(validators=[MinValueValidator(0),MaxValueValidator(5)])
    user    = models.ForeignKey(User,on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username

class UserLike(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)
    def __str__(self):
        return self.user.username+self.meal.meal_name