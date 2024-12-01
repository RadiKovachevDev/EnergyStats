from django.urls import path
from . import views

urlpatterns = [
    path('', views.prices_view, name='prices_view'),
    path('prices/<str:date>/', views.price_details_view, name='price_details'),
]
