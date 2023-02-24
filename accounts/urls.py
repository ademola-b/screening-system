
from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('login/', views.login_request, name='login'),
    path('logout/', views.login_request, name='logout')
    
]
