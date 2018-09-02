from django.shortcuts import render,HttpResponseRedirect
from django.db.models import Q
from meal.models import *
from user_profile.models import UserProfile,ChiefProfile
from .models import Transactions
from django.views.generic import DetailView,UpdateView,CreateView,View
from django.contrib.auth.mixins import LoginRequiredMixin
from unidecode import unidecode
from operator import itemgetter

class most_search_meals(LoginRequiredMixin,View):
    def get(self, request, **kwargs):
        template_name   = "most_search.html"
        qs_user = UserProfile.objects.filter(user__username=self.request.user)
        transactions = Transactions.objects.all()
        meals = Meal.objects.all()
        meals_count = []
        for meal in meals:
            count = Transactions.objects.filter(result__meal_name__icontains=meal.meal_name).count()
            meals_count.append([meal, count])
        final = sorted(meals_count, key=itemgetter(1), reverse=True)
        if not qs_user:
            return HttpResponseRedirect('/Home/chief')
        context = {
            'transactions': final[:5]
        }

        return render(request, template_name, context)

class user_like_meals(LoginRequiredMixin,View):
    def get(self, request, **kwargs):
        template_name   = "most_liked.html"
        qs_user = UserProfile.objects.filter(user__username=self.request.user)
        meals = Meal.objects.all()
        likes = UserLike.objects.filter(user__username = self.request.user)
        liked_meals = []
        for meal in meals:
            for like in likes:
                if like.meal.id == meal.id:
                    liked_meals.append(meal)
        context = {
            'transactions': liked_meals
        }
        if not qs_user:
            return HttpResponseRedirect('/Home/chief')
        return render(request, template_name, context)

def search_by_meal_name(request):
    template = 'search_by_ingredients.html'
    ingred = Ingredient.objects.all()
    query = request.GET.get('q')
    if query != None and query != " " and query != "":
        results = Meal.objects.filter(Q(meal_name__icontains=query)) #| Q(meal_recipe__icontains=query)
    else:
        results = Meal.objects.none()

    qs = ChiefProfile.objects.filter(user__username=request.user)
    context = {
        'meals': results,
        'profile_info': qs,
        'group': "chief",
        "ingredients": ingred,
        "msg": "بهذا الاسـم"
    }
    if not qs:
        qs = UserProfile.objects.filter(user__username=request.user)
        context['profile_info'] = qs
        context['group'] = "user"

        if request.user.is_authenticated:
            obj = Transactions.objects.create(
                user = request.user,
                search_context = query
            )
            obj.result.add(*results)
    return render(request, template, context)

def search_by_ingredients(request):
    template = 'search_by_ingredients.html'
    qs = UserProfile.objects.filter(user__username=request.user)
    ingred = Ingredient.objects.all()
    query = request.GET.getlist('query')
    ings = []
    ings_names = []
    if query != None:
        query_ingredients = query[0].split(',')

        for i in query_ingredients:
            ingredients = Ingredient.objects.filter(ingredient_name=i)
            for ing in ingredients:
                ings.append(ing.id)
                ings_names.append(ing)
        meal = Meal.objects.filter(ingredients__in=ings).distinct()

    else:
        meal = Meal.objects.none()

    categories = Category.objects.all()
    context = {
        'meals': meal,
        'ingredients_list':ings_names,
        'profile_info': qs,
        'group': "user",
        "ingredients": ingred,
        "msg": "بهذه المـكونـات",
        'categories':categories
    }
    if request.user.is_authenticated:
        obj = Transactions.objects.create(
            user = request.user,
            search_context=query
        )
        obj.result.add(*meal)
    return render(request, template, context)

class view_history(LoginRequiredMixin,View):
    def get(self,request,**kwargs):
        template_name = "history.html"
        qs_user = UserProfile.objects.filter(user__username=self.request.user)
        if qs_user:
            transactions = Transactions.objects.filter(user = request.user).order_by('-id')
            context = {
                "profile_info": qs_user,
                "group": "user",
                'transactions': transactions
            }
            return render(request, template_name, context)
        else:
            return HttpResponseRedirect('/')

class view_result(LoginRequiredMixin,View):
    def get(self,request,**kwargs):
        template_name = "result.html"
        qs_user = UserProfile.objects.filter(user__username=self.request.user)
        if qs_user:
            t_id = kwargs['pk']
            transaction = Transactions.objects.filter(id=t_id)
            ingred = Ingredient.objects.all()
            context = {
                "profile_info": qs_user,
                "group": "user",
                'transaction': transaction,
                "ingredients": ingred,
            }
            return render(request, template_name, context)

def delete_trans(request,**kwargs):
    t_id = kwargs['pk']
    transaction =  Transactions.objects.get(id=t_id)
    if transaction.user == request.user:
        transaction.delete()
    return HttpResponseRedirect('/')

def clear_history(request,**kwargs):
    transaction =  Transactions.objects.filter(user = request.user).delete()
    return HttpResponseRedirect('/')