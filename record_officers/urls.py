from django.urls import path
from . import views
from . views import homepage, FirstScreeningList, FirstScreeningDetail, record_officer_first_modify, SecondScreeningList, SecondScreeningDetail

app_name = 'record_officer'
urlpatterns = [
    path('', homepage, name='home'),
    path('first-screening/', FirstScreeningList.as_view(), name='first_screening'),
    path('first-screening/<int:pk>/', FirstScreeningDetail.as_view(), name = "screening_detail"),
    path('first-screening-modify/<int:id>/', record_officer_first_modify, name='modify_screening'),
    path('second-screening/', SecondScreeningList.as_view(), name='second_screening'),
    path('second-screening/<int:pk>/', SecondScreeningDetail.as_view(), name = "second_screening_detail"),
    path('second-screening-modify/<int:id>/', views.record_officer_second_modify, name='second_screening_modification')

]