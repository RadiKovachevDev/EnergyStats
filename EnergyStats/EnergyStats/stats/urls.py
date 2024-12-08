from django.urls import path
from . import views

urlpatterns = [
    path('', views.statistics_view, name='statistics'),

    path('statistics/weekly/', views.weekly_statistics_view, name='weekly_statistics'),
    path('statistics/monthly/', views.monthly_statistics_view, name='monthly_statistics'),
    path('statistics/yearly/', views.yearly_statistics_view, name='yearly_statistics'),
]
