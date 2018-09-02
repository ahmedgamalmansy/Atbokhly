from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from django.contrib.auth.models import User,Group
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.views.generic import UpdateView, View, CreateView, DetailView,ListView
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage,send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
import unidecode
from user_profile.models import *
from meal.models import *
from Contact.models import *
from .form import *


def admin_login(request):
    if request.user.is_authenticated:
        return redirect('admin_pannel:home')
    else:
        form = LoginForm(request.POST or None)
        if form.is_valid():
            user_name = form.cleaned_data.get('user_name')
            password  = form.cleaned_data.get('password')
            obj = User.objects.filter(username=user_name)

            if obj:
                user = authenticate(request, username=user_name, password=password)
                if user and user.is_superuser:
                    login(request, user)
                    return redirect('admin_pannel:home')
                else:
                    messages.error(request, 'Incorrect username or password')

        template_name = 'auth/ad_login.html'
        context = {
            "form":form,
        }
        return render(request,template_name,context)



def user_logout(request):
    logout(request)
    return redirect('admin_pannel:admin-login')




class UpdateProfile(LoginRequiredMixin,UpdateView):
    template_name = 'auth/update_profile.html'
    login_url = reverse_lazy('admin_pannel:login')
    model = User
    fields = [
        'first_name',
        'last_name'
    ]
    success_url = reverse_lazy('admin_pannel:home')



def admin_home(request, **kwargs):
    template        = 'admin_home.html'
    chef_count      = ChiefProfile.objects.all().count()
    user_count      = UserProfile.objects.all().count()
    meal_count      = Meal.objects.all().count()
    visits          = Visitors.objects.all()
    last_month      = visits.last().number
    visits_count    = 0

    for v in visits:
        visits_count += v.number

    context = {
        'chef_count': chef_count,
        'user_count': user_count,
        'meal_count': meal_count,
        'visits'    : [last_month,visits_count]
    }
    return render(request,template,context)



User = get_user_model()

class ChartView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return render(request, 'charts.html')
        else:
            return HttpResponse('<h1>Page not found</h1>')



class ChartData(APIView):
    authentication_classes = []
    permission_classes = []
    def get(self, request, format=None):
        labels          = []
        default_items   = []
        chiefs          = ChiefProfile.objects.all()

        for chief in chiefs:
            chief_obj           = User.objects.get(username=chief.user)
            chief_meals         = Meal.objects.filter(meal_owner=chief_obj)
            chief_meals_count   = Meal.objects.filter(meal_owner=chief_obj).count()
            chief_mean_rates    = 0

            for meal in chief_meals:
                meal_rate        = Rate.objects.filter(meal=meal)
                chief_mean_rates = chief_mean_rates + float(meal_rate[0].rate_value)

            if chief_meals_count == 0:
                chief_mean_rates = round(chief_mean_rates / 1, 2)

            else:
                chief_mean_rates = round(chief_mean_rates / chief_meals_count, 2)
            labels.append(chief_obj.first_name+" "+chief_obj.last_name)
            default_items.append(chief_mean_rates)

        data = {
                "labels": labels,
                "default": default_items,
        }
        return Response(data)



class ChartUserData(APIView):
    authentication_classes  = []
    permission_classes      = []
    def get(self, request, format=None):
        labels          = []
        default_items   = []
        normal_users    = User.objects.filter(groups__name='normal_users').order_by('date_joined')
        month           = ""

        for user in normal_users:
            user_count = User.objects.filter(groups__name='normal_users', date_joined__month=int(user.date_joined.strftime('%m')),date_joined__year=user.date_joined.year).count()
            if user.date_joined.strftime('%m') + " - " + str(user.date_joined.year) == month:
                pass
            else:
                month = user.date_joined.strftime('%m') + " - " + str(user.date_joined.year)
                labels.append(month)
                default_items.append(user_count)

        data = {
            "labels": labels,
            "default": default_items,
        }
        return Response(data)



class ChartVisitsData(APIView):
    authentication_classes = []
    permission_classes = []
    def get(self, request, format=None):
        labels = []
        default_items = []
        visits = Visitors.objects.all()
        for visit in visits:
            # print('the month is => ', visit.timestamp.strftime('%m'))
            # print('the number is => ', visit.number)
            labels.append(visit.timestamp.strftime('%m')+" - "+visit.timestamp.strftime('%y'))
            default_items.append(visit.number)

        data = {
                "labels": labels,
                "default": default_items,
        }

        return Response(data)



class Add_Category(LoginRequiredMixin,CreateView):
    template_name   = "add_cat.html"
    login_url       = reverse_lazy('accounts:login')
    model           = Category
    fields          = '__all__'
    success_url     = reverse_lazy('admin_pannel:home')



class Add_Ingredient(LoginRequiredMixin,CreateView):
    template_name   = "add_cat.html"
    login_url       = reverse_lazy('accounts:login')
    model           = Ingredient
    fields          = '__all__'
    success_url     = reverse_lazy('admin_pannel:home')



class View_Meals(LoginRequiredMixin,ListView):
    template_name   = 'meals.html'
    model           = Meal
    def get_context_data(self, **kwargs):
        context         = super(View_Meals, self).get_context_data(**kwargs)
        context['meal'] = 'meal'
        return context

class View_Categories(LoginRequiredMixin,ListView):
    template_name= 'meals.html'
    model = Category

    def get_context_data(self, **kwargs):
        context = super(View_Categories, self).get_context_data(**kwargs)

        context['cat'] = 'cat'

        return context



class View_Ingredients(LoginRequiredMixin,ListView):
    template_name= 'meals.html'
    model = Ingredient

    def get_context_data(self, **kwargs):
        context = super(View_Ingredients, self).get_context_data(**kwargs)

        context['ing'] = 'ing'

        return context

class View_Contacts(LoginRequiredMixin,View):
    def get(self, request, **kwargs):
        template_name = "contacts.html"
        if self.request.user.is_superuser:
            qs = Contact.objects.filter(state=None)
            context = {
                'contacts': qs
            }
            return render(request, template_name, context)
        else:
            return redirect("/")



class View_Contact(LoginRequiredMixin,View):
    def get(self, request, **kwargs):
        c_id = kwargs['pk']
        template_name = "contact_details.html"
        if self.request.user.is_superuser:
            qs = Contact.objects.filter(id=c_id)
            qs.update(state=True)
            context = {
                'contact': qs
            }
            return render(request, template_name, context)
        else:
            return redirect("/")


class View_all_Contacts(LoginRequiredMixin,View):
    def get(self, request, **kwargs):
        template_name = "contacts.html"
        if self.request.user.is_superuser:
            qs = Contact.objects.all()
            context = {
                'contacts': qs,
                'all': 'all'
            }
            return render(request, template_name, context)
        else:
            return redirect("/")


class View_Requests(LoginRequiredMixin,View):
    def get(self, request, **kwargs):
        if self.request.user.is_superuser:
            template_name   = 'requests.html'
            req             = ChiefProfile.objects.filter(state=None)
            return render(request, template_name, {'req':req})
        else:
            return redirect('/')


class Respond_Reuests(LoginRequiredMixin,View):
    def get(self, request, **kwargs):
        if self.request.user.is_superuser:
            form = respond_request(request.GET or None)
            item_id         = kwargs['pk']
            template_name   = 'request_response.html'
            chef             = ChiefProfile.objects.filter(pk=item_id)
            if form.is_valid():
                state = form.cleaned_data.get('state')
                chef.update(state=state)
                current_site = get_current_site(request)
                if state == True:
                    print(True)
                    message = render_to_string('respond_req.html', {
                                'user': chef[0],
                                'state': state,
                                'domain': current_site.domain,
                            })
                else:
                    print(False)
                    message = render_to_string('respond_req.html', {
                        'user': chef[0],
                        'state': state,
                        'domain': current_site.domain,
                    })

                send_mail("Request response", message, settings.EMAIL_HOST_USER, [chef[0].email], fail_silently=False)
                return redirect('admin_pannel:view-chef-Requests')
            context = {
                'chef': chef[0],
                'form': form
            }
            return render(request, template_name, context)
        else:
            return redirect('/')



def delete_category(request, **kwargs):
    if request.user.is_superuser:
        Category.objects.filter(id=kwargs['pk']).delete()
        return redirect('admin_pannel:view-categories')
    else:
        return redirect('/')


def delete_ingredient(request, **kwargs):
    if request.user.is_superuser:
        Ingredient.objects.filter(id=kwargs['pk']).delete()
        return redirect('admin_pannel:view-ingredients')
    else:
        return redirect('/')



class Update_Cat(LoginRequiredMixin,UpdateView):
    template_name = 'edit.html'
    login_url = reverse_lazy('admin_pannel:login')
    model = Category
    fields = ['category_name']
    success_url = reverse_lazy('admin_pannel:view-categories')
    def get_context_data(self, **kwargs):
        context = super(Update_Cat, self).get_context_data(**kwargs)
        context['cat'] = 'cat'
        return context





class Update_Ing(LoginRequiredMixin,UpdateView):
    template_name = 'edit.html'
    login_url = reverse_lazy('admin_pannel:login')
    model = Ingredient
    fields = '__all__'
    success_url = reverse_lazy('admin_pannel:view-ingredients')

    def get_context_data(self, **kwargs):
        context = super(Update_Ing, self).get_context_data(**kwargs)
        context['ing'] = 'ing'
        return context


class View_Chefs(LoginRequiredMixin,View):
    def get(self, request, **kwargs):
        template    = 'view_chef.html'
        chefs       = ChiefProfile.objects.all()
        context     = {
            'chefs': chefs,
            'user_obj': 'chefs'
        }
        return render(request,template, context)


class Chef_State(LoginRequiredMixin,View):
    def get(self, request, **kwargs):
        if(request.user.is_superuser):
            ch_id        = kwargs['pk']
            chef         = User.objects.filter(groups__name='chiefs', id=ch_id)
            current_site = get_current_site(request)

            if chef[0].is_active == True:
                chef.update(is_active=False)
                message = render_to_string('bann_mail.html', {
                    'username': chef[0].username,
                    'domain': current_site.domain,
                    'state': 'false'
                })
            elif chef[0].is_active == False:
                chef.update(is_active=True)
                message = render_to_string('bann_mail.html', {
                    'username': chef[0].username,
                    'domain': current_site.domain,
                    'state': 'true'
                })

            send_mail('email got banned', message, settings.EMAIL_HOST_USER, [chef[0].email], fail_silently=False)
            return redirect('admin_pannel:view-chefs')
        else:
            return redirect('/')


class View_Users(LoginRequiredMixin,View):
    def get(self, request, **kwargs):
        template    = 'view_chef.html'
        chefs       = UserProfile.objects.all()
        context     = {
            'chefs': chefs,
            'user_obj': 'users'
        }
        return render(request,template, context)


class User_State(LoginRequiredMixin,View):
    def get(self, request, **kwargs):
        if(request.user.is_superuser):
            ch_id = kwargs['pk']
            user = User.objects.filter(groups__name='normal_users', id=ch_id)
            current_site = get_current_site(request)

            if user[0].is_active == True:
                user.update(is_active=False)
                message = render_to_string('bann_mail.html', {
                    'username': user[0].username,
                    'domain': current_site.domain,
                    'state' : 'false'
                })
            elif user[0].is_active == False:
                user.update(is_active=True)
                message = render_to_string('bann_mail.html', {
                    'username': user[0].username,
                    'domain': current_site.domain,
                    'state' : 'true'
                })

            print(message)
            send_mail('email got banned', message, settings.EMAIL_HOST_USER, [user[0].email], fail_silently=False)
            return redirect('admin_pannel:view-users')
        else:
            return redirect('/')