from django.urls import path
from . import views

app_name = 'student_affair'
urlpatterns = [
    path('', views.homepage, name='home')
]
