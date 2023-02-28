from django.urls import path
from . import views

app_name = 'student_affair'
urlpatterns = [
    path('', views.homepage, name='home'),
    path('first-screening', views.FirstScreeningList.as_view(), name='first_screening'),
    path('first-screening/<int:pk>/', views.FirstScreeningDetail.as_view(), name='first_screening_detail'),
    path('first-screening-modify/<int:id>/', views.fscreening_modify, name='modify_first_screening')
    
]
