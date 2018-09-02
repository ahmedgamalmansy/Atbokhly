from django.urls import path
from search.views import *

app_name='search'
urlpatterns = [
    path('search-by-meal-name/', search_by_meal_name, name='search_by_meal_name'),
    path('search-by-ingredients/', search_by_ingredients, name='search_by_ingredients'),
    path('most-search-meals/<int:pk>', most_search_meals.as_view(), name='most-search-meals'),
    path('most-liked-meals/<int:pk>', user_like_meals.as_view(), name='most-liked-meals'),
    path('history/', view_history.as_view(), name='view_history'),
    path('result/<int:pk>', view_result.as_view(), name='view_search_result'),
    path('delete-transaction/<int:pk>', delete_trans, name='delete-transaction'),
    path('clear/', clear_history, name='clear'),
    #path('meal/<slug:slug>/', meal.as_view(template_name='meal.html'), name='meal'),
]