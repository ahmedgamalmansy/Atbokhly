from django.shortcuts import render,redirect

import user_profile
from .models import *
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView,View
from django.urls import reverse_lazy
from django.contrib.auth.models import User,Group
from meal.models import Meal,Category,Rate,UserLike,Ingredient,UserRate
from search.models import Transactions
from operator import itemgetter
from unidecode import unidecode
import json
from django.core import serializers
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage,send_mail
from django.conf import settings
from .form import *
import datetime
from django.utils.timezone import utc
# Create your views here.


def chief_home(request):
    if request.user.is_authenticated:
        chef = User.objects.filter(groups__name='chiefs', username=request.user)
        if chef:
            qs = ChiefProfile.objects.filter(user=request.user)
            if not qs:
                query = User.objects.filter(username=request.user)
                ChiefProfile.objects.create(
                    user=request.user,
                    first_name=query[0].first_name,
                    last_name=query[0].last_name,
                    email=query[0].email,
                )

            template_name = 'user_profile/chief_home.html'
            meals = Meal.objects.filter(meal_owner=request.user)
            categ = Category.objects.all()
            rates = Rate.objects.all()
            chef_state = ChiefProfile.objects.filter(user__username=request.user)
            for i in rates:
                i.rate_value = round(i.rate_value,2)
            context       = {
                'meals': meals,
                'categories': categ,
                'rates': rates,
                'state':chef_state[0].state
            }

            return render(request,template_name,context)
        else:
            return redirect('/')
    else:
        return redirect('accounts:login')


class UpdateChiefProfile(LoginRequiredMixin,UpdateView):
    template_name = 'user_profile/update_profile.html'
    login_url = reverse_lazy('accounts:login')
    model = ChiefProfile
    fields = [
        'first_name',
        'last_name',
        'gender',
        'date_birth',
        'phone',
        'img',
        'cv'
    ]
    success_url = reverse_lazy('user_profile:chief-home')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        chef_state = ChiefProfile.objects.filter(user__username=self.request.user)
        created_at          = chef_state[0].timestamp
        now = datetime.datetime.utcnow().replace(tzinfo=utc)
        diff_time = (now - created_at).days
        context['state'] = chef_state[0].state
        context['diff_time'] = diff_time
        return context

    def get_queryset(self):
        name = dict(self.request.POST)
        for k in name:
            name[k] = "".join(name[k])
        fname       = name.get('first_name')
        lname       = name.get('last_name')
        obj         = User.objects.filter(username=self.request.user)
        chef_state = ChiefProfile.objects.filter(user__username=self.request.user)
        if chef_state[0].state != True and name.get('submit') == "":
            print(chef_state[0].state)
            chef_state.update(state=None, timestamp=timezone.now())

        queryset = super().get_queryset()
        if fname and lname :
            obj.update(first_name=fname,last_name=lname)
        return queryset.filter(user=self.request.user)


def user_home(request):
    template_name = 'user_profile/user_home.html'
    categ = Category.objects.all()
    count = categ.count()
    meals = Meal.objects.all()

    # get top rated meals
    top_records = []
    for cat in categ:
        cat_meals = Meal.objects.filter(meal_category=cat)
        top = Rate.objects.order_by('-rate_value').filter(meal__in=cat_meals)
        for t in top[:10]:
            top_records.append(t)
    for i in top_records:
        i.rate_value = round(i.rate_value, 2)

    # update the site visits count
    date    = Visitors.objects.all()
    now     = datetime.datetime.utcnow().replace(tzinfo=utc)
    if date:
        diff    = now - date.last().timestamp
        if diff.days > 30:
            Visitors.objects.create(number=1)
        else:
            obj = Visitors.objects.all()

            last_num = obj.last().number
            Visitors.objects.filter(id=obj.last().id).update(number=last_num+1)
    else:
        Visitors.objects.create(number=1)

    # get the recommended meals
    meals_count = []
    like = UserLike.objects.filter(user__username=request.user)
    q = UserLike.objects.raw('SELECT id,meal_id,COUNT(meal_id) AS meal_count FROM meal_UserLike GROUP BY meal_id')
    for i in q:
        meal_obj = Meal.objects.get(id=i.meal_id)
        meals_count.append([meal_obj,i.meal_count])
    final = sorted(meals_count, key=itemgetter(1), reverse=True)
    ing = Ingredient.objects.all()
    context = {
        'top_records': top_records,
        'categories': categ,
        'meals': meals,
        'transactions': final[:5],
        'likes': like,
        "ingredients": ing
    }
    if request.user.is_authenticated:
        user = User.objects.filter(groups__name='normal_users',username=request.user)
        if user:
            qs = UserProfile.objects.filter(user=request.user)
            if not qs:
                query = User.objects.filter(username=request.user)
                UserProfile.objects.create(
                    user=request.user,
                    first_name=query[0].first_name,
                    last_name=query[0].last_name,
                    email=query[0].email,
                )

        is_admin = User.objects.filter(username=request.user)
        if not user and not is_admin[0].is_superuser:
            return HttpResponseRedirect('/Home/chief')
    return render(request, template_name, context)


class UpdateUserProfile(LoginRequiredMixin,UpdateView):
    template_name = 'user_profile/update_profile.html'
    login_url = reverse_lazy('accounts:login')
    model = UserProfile
    fields = [ 'first_name' , 'last_name' , 'gender' , 'date_birth' , 'phone' , 'img' ]
    success_url = reverse_lazy('user_profile:home')
    def get_queryset(self):
        name = dict(self.request.POST)
        for k in name:
            name[k] = "".join(name[k])
        fname = name.get('first_name')
        lname = name.get('last_name')
        obj = User.objects.filter(username=self.request.user)
        if fname and lname:
            obj.update(first_name=fname, last_name=lname)

        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)


class view_user_profile(LoginRequiredMixin,View):
    def get(self, request, **kwargs):
        qs_user = UserProfile.objects.filter(user__username=self.request.user)
        context = { "users": qs_user }
        return render(request, 'user_profile/view_chief_profile.html', context)


class view_chief_profile(View):
    def get(self, request, **kwargs):
        user_id     = kwargs['pk']
        user = User.objects.filter(id = user_id)
        if user[0].is_superuser:
            print('equal')
            context = {"users": user}
        else:
            qs_chef = ChiefProfile.objects.filter(user__id=user_id)
            context = {"users": qs_chef}
            if qs_chef and not qs_chef[0].state:
                return HttpResponseRedirect('/Home/chief')

        return render(request, 'user_profile/view_chief_profile.html', context)



class View_chief_meals(View):
    def get(self, request, **kwargs):
        chief_id    = kwargs['pk']
        meals       = Meal.objects.filter(meal_owner__id= chief_id)
        categories  = Category.objects.all()
        rates       = Rate.objects.all()
        chef        = ChiefProfile.objects.filter(user__id=chief_id)
        if chef:
            chef_state  = chef[0].state
        else:
            chef_state = None

        for i in rates:
            i.rate_value = round(i.rate_value, 2)
        context = {
            'meals': meals,
            'categories': categories,
            'rates': rates,
            'state': chef_state
        }
        return render(request, 'user_profile/view_chief_meals.html', context)


def update_email(request,**kwargs):
    form = email_update_form(request.GET or None)
    template_name = 'user_profile/update_email.html'
    user = User.objects.filter(username=request.user)
    errors = None
    if form.is_valid():
        email = form.cleaned_data.get('email')
        if (email != user[0].email and not User.objects.filter(email=email)) or (email == user[0].email and User.objects.filter(email=email).count() <= 1):
            if email == user[0].email:
                return redirect('/')
            current_site = get_current_site(request)
            mail_subject = 'Activate your Atbokhly new email.'
            message = render_to_string('user_profile/acc_active_email.html', {
                'user': user[0],
                'uid': urlsafe_base64_encode(force_bytes(request.user.id)).decode(),
                'email': email,
                'domain': current_site.domain,
                'token': account_activation_token.make_token(user),
            })
            to_email = email
            send_mail( mail_subject, message, settings.EMAIL_HOST_USER, [to_email], fail_silently=False)
            return HttpResponseRedirect('/email-confirm')
        else:
            errors = 'this email already exists'
    else:
        errors = form.errors
    context = {
        'form': form,
        'errors': errors,
    }
    chef_state = ChiefProfile.objects.filter(user=request.user)
    if chef_state:
        context['state'] = chef_state[0].state

    return render(request,template_name,context)



def activate(request, uidb64, token, email):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.filter(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.update(email=email)
        chief = ChiefProfile.objects.filter(user=request.user)
        normal_user = UserProfile.objects.filter(user=request.user)
        if chief:
            chief.update(email=email)
        elif normal_user:
            normal_user.update(email=email)
        else:
            pass
        return HttpResponseRedirect('/email-success')
    else:
        return HttpResponse('Activation link is invalid!')


def email_confirm(request):
    return render(request,'user_profile/registration_confirm_msg.html',{})
def email_success(request):
    return render(request,'user_profile/registration_success.html',{})