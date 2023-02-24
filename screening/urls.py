from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'screening'
urlpatterns = [
    path('', views.onboard, name='onboard'),
    path('index/', views.index, name='index'),
    path('first-screening/', views.FirstScreeningForm.as_view(), name='first_screening'),
    path('first-screening-view/', views.firstScreeningView, name='first_screening_view'),

    path('second-screening/', views.SecondScreeningForm.as_view(), name='second_screening'),
    path('second-screening-view/', views.secondScreeningView, name='second_screening_view'),  
]