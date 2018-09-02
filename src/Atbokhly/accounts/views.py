from .form import *
from django.contrib.auth.models import User,Group
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect,HttpResponseRedirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage,send_mail
from django.conf import settings
from user_profile.models import *
import datetime
from django.utils.timezone import utc
# Create your views here.

def login_fun(request,user, password):
    user = authenticate(request, username=user, password=password)
    if user is not None:
        if not user.is_superuser:
            login(request, user)
            cheifs = Group.objects.get(name="chiefs").user_set.all()
            for cheif in cheifs:
                if request.user == cheif:
                    return 'user_profile:chief-home'
            else:
                return 'user_profile:home'
        else:
            messages.error(request, 'Incorrect username or password')
    else:
        messages.error(request, 'Incorrect username or password')


def user_login(request):
    if request.user.is_authenticated:
        cheifs = Group.objects.get(name="chiefs").user_set.all()
        normal_users = Group.objects.get(name="normal_users").user_set.all()
        for cheif in cheifs:
            if request.user == cheif:
                return redirect('user_profile:chief-home')
        for user in normal_users:
            if request.user == user:
                return redirect('user_profile:home')
    else:
        form = LoginForm(request.POST or None)
        now = datetime.datetime.utcnow().replace(tzinfo=utc)
        if form.is_valid():
            user_name = form.cleaned_data.get('user_name')
            password  = form.cleaned_data.get('password')
            obj = User.objects.filter(username=user_name)
            last_login = None
            if obj:
                last_login = obj[0].last_login
            if last_login:
                b = now - last_login
                if authenticate(request,username=user_name,password=password) and int(b.days) > 90:
                    messages.error(request,'Sorry *'+obj[0].username+'* your account has been banned since you did not login for more than 90 days you can contact us to return it back')
                # elif :
                #     messages.error(u'sorry you account got banned not active if you did not activate it please do it through the confirmation mail we sent you')
                elif not authenticate(request,username=user_name,password=password):
                    messages.error(request, 'Incorrect username or password')
                else:
                    path = login_fun(request, user_name, password)
                    if path:
                        return redirect(path)
            else:
                path = login_fun(request, user_name, password)
                if path:
                    return redirect(path)
        template_name = 'auth/login.html'
        context = {
            "form":form,
        }
        return render(request,template_name,context)



def user_register(request):
    template_name = 'auth/register.html'
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = RegisterForm(request.POST, request.FILES)
            if form.is_valid():
                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')
                user_name = form.cleaned_data.get('user_name')
                email = form.cleaned_data.get('email')
                password = form.cleaned_data.get('password')
                type = form.cleaned_data.get('user_type')
                cv = form.cleaned_data['cv']
                User.objects.create_user(
                    username=user_name,
                    password=password,
                    email=email
                )
                obj = User.objects.filter(username=user_name)
                obj.update(first_name=first_name, last_name=last_name,is_active=False)

                if type == 'cheif':
                    cheifs_group = Group.objects.get(name='chiefs')
                    user = User.objects.get(username=user_name)
                    cheifs_group.user_set.add(user)
                    ChiefProfile.objects.create(
                        user=obj[0],
                        first_name=first_name,
                        last_name=last_name,
                        email=email,
                        cv=cv
                    )
                if type == 'normal_user':
                    normal_users_group = Group.objects.get(name='normal_users')
                    user = User.objects.get(username=user_name)
                    normal_users_group.user_set.add(user)
                    UserProfile.objects.create(
                        user=obj[0],
                        first_name=first_name,
                        last_name=last_name,
                        email=email
                    )

                current_site = get_current_site(request)
                mail_subject = 'Activate your Atbokhly account.'
                message = render_to_string('auth/acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                    'token': account_activation_token.make_token(user),
                })
                to_email = email

                send_mail(
                    mail_subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [to_email],
                    fail_silently=False,
                )
                return HttpResponseRedirect('/auth/registration-confirm')
        else:
            form = RegisterForm()

        context       = {
            'form':form,

        }
        return render(request,template_name,context)
    else:
        return redirect('accounts:login')


def user_logout(request):
    logout(request)
    return redirect('user_profile:home')

def change_password(request):
    if request.user.is_authenticated:
        form = PasswordChangeForm(request.user,request.POST or None)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('accounts:logout')
        else:
            messages.error(request, 'Please correct the error below.')
        template_name = 'auth/change_password.html'


        context = {
            "form": form
        }
        q_user = ChiefProfile.objects.filter(user__username=request.user)
        qs = ChiefProfile.objects.filter(user__username=request.user)
        # if q_user and not qs[0].state:
        #     return HttpResponseRedirect('/Home/chief')

        return render(request,template_name,context)
    else:
        return redirect('accounts:login')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponseRedirect('/auth/registration-success')
    else:
        return HttpResponse('Activation link is invalid!')


def registration_confirm(request):
    return render(request,'auth/registration_confirm_msg.html',{})
def registration_success(request):
    return render(request,'auth/registration_success.html',{})