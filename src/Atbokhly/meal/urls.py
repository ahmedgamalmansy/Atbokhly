from django.urls import path
from meal.views import *

app_name='meal'
urlpatterns = [
    path('<int:pk>/', meal_new.as_view(), name='meal'),
    path('<int:pk>/rate', rate, name='rate'),
    path('<int:pk>/like', userlike, name='like'),

    path('<int:pk>/comment', comment, name='comment'),
    path('<int:pk>/reply-comment', reply, name='reply-comment'),
    path('<int:pk>/like-comment', comment_like, name='like-comment'),
    path('<int:pk>/like-reply', reply_like, name='-like-reply'),

    path('<int:pk>/feedback/', feedback.as_view(), name='feedback'),
    path('<int:pk>/add-meal/', AddMeal.as_view(), name='addmeal'),
    path('delete-meal/<int:pk>', deleteMeal, name='deletemeal'),
    path('update-meal/<int:pk>', UpdateMeal.as_view(), name='update-emeal'),
    path('meal-feedback/<int:pk>', ViewFeedback, name='meal-feedback'),
    path('meal-feedback/details/<int:pk>', FeedbackDetails.as_view(), name='feedback-details'),
]