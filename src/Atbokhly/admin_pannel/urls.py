from django.urls import path
from django.conf.urls import url
from .views import *
# from accounts.views import change_password
from django.contrib.auth.views import password_reset, password_reset_done, password_reset_confirm, password_reset_complete

app_name='admin_pannel'
urlpatterns = [
    path('admin-login/',admin_login , name='admin-login'),
    path('logout',user_logout,name='logout'),
    path('reset-password', password_reset,
    {'template_name': 'auth/reset_password.html', 'post_reset_redirect': 'accounts:password_reset_done',
    'email_template_name': 'auth/reset_password_email.html'}, name='reset_password'),

    path('home/',admin_home , name='home'),


    path('<int:pk>/update-profile',UpdateProfile.as_view(),name='update-profile'),


    path('chart/',ChartView.as_view(),name='chart_view'),
    path('api/chart/data/',ChartData.as_view()),
    path('api/chart_visits/data/',ChartVisitsData.as_view()),
    path('api/chart_user/data/',ChartUserData.as_view()),

    path('add-category',Add_Category.as_view() ,name='add-category'),
    path('add-ingredient',Add_Ingredient.as_view() ,name='add-ingredient'),

    path('view-meals',View_Meals.as_view() ,name='view-meals'),

    path('view-ingredients',View_Ingredients.as_view() ,name='view-ingredients'),
    path('<int:pk>/delete-ingredient',delete_ingredient ,name='delete-ingredient'),
    path('<int:pk>/edit-ingredient',Update_Ing.as_view() ,name='edit-ingredient'),

    path('view-categories',View_Categories.as_view() ,name='view-categories'),
    path('<int:pk>/edit-category',Update_Cat.as_view() ,name='edit-category'),
    path('<int:pk>/delete-category',delete_category ,name='delete-category'),


    path('view-contacts',View_Contacts.as_view() ,name='view-contacts'),
    path('<int:pk>/view-contact',View_Contact.as_view() ,name='view-contact'),
    path('view-all-contacts',View_all_Contacts.as_view() ,name='view-all-contacts'),


    path('view-chefs',View_Chefs.as_view() ,name='view-chefs'),
    path('view-users',View_Users.as_view() ,name='view-users'),
    path('<int:pk>/edit-chef-state',Chef_State.as_view() ,name='edit-state'),
    path('<int:pk>/edit-user-state',User_State.as_view() ,name='edit-user-state'),

    path('view-chef-Requests',View_Requests.as_view() ,name='view-chef-Requests'),
    path('<int:pk>/respond-chef-request',Respond_Reuests.as_view() ,name='respond-chef-request'),
]