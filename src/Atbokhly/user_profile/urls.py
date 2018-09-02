from django.urls import path
from django.conf.urls import url
from .views import *

app_name='user_profile'
urlpatterns = [
        path('Home/chief/',chief_home,name='chief-home'),
        # path('Home/',user_home,name='user-home'),
        path('',user_home,name='home'),
        path('<int:pk>/view-user-profile',view_user_profile.as_view(),name='user-view-profile'),
        path('view-chief-meals/<int:pk>',View_chief_meals.as_view(),name='view-chief-meals'),
        path('<int:pk>/view-chief-profile',view_chief_profile.as_view(),name='chief-view-profile'),
        path('<int:pk>/update-profile',UpdateChiefProfile.as_view(),name='chief-update-profile'),
        path('<int:pk>/update-user-profile',UpdateUserProfile.as_view(),name='user-update-profile'),
        url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/(?P<email>[\w.@+-_]+)/$', activate, name='activate'),
        path('email-update',update_email,name='update-email'),
        path('email-confirm',email_confirm,name='email-confirm'),
        path('email-success',email_success,name='email-success')
]