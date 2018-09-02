from django.urls import path
from django.conf.urls import url
from .views import *
from django.contrib.auth.views import password_reset, password_reset_done, password_reset_confirm, password_reset_complete
from user_profile.views import user_home

app_name='accounts'
urlpatterns = [
    path('login',user_login,name='login'),
    path('logout',user_logout,name='logout'),
    path('register',user_register,name='register'),
    path('change-password',change_password,name='change-password'),
    path('reset-password', password_reset,
    {'template_name': 'auth/reset_password.html', 'post_reset_redirect': 'accounts:password_reset_done',
    'email_template_name': 'auth/reset_password_email.html'}, name='reset_password'),
    path('reset-password/done', password_reset_done, {'template_name': 'auth/reset_password_done.html'}, name='password_reset_done'),
    url(r'^reset-password/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', password_reset_confirm, {'template_name': 'auth/reset_password_confirm.html', 'post_reset_redirect': 'accounts:password_reset_complete'} ,name='password_reset_confirm'),
    path('reset-password/complete', password_reset_complete, {'template_name': 'auth/reset_password_complete.html'}, name='password_reset_complete'),
    # path('signup', signup, name='signup'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', activate, name='activate'),
    path('registration-confirm',registration_confirm,name='registration-confirm'),
    path('registration-success',registration_success,name='registration-success')
]