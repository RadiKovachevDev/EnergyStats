from django.urls import path
from . import views

urlpatterns = [
    path('', views.prices_view, name='prices_view'),
]
