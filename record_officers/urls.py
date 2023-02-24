from django.urls import path

from . views import homepage, FirstScreeningList, FirstScreeningDetail, record_officer_modify

app_name = 'record_officer'
urlpatterns = [
    path('', homepage, name='home'),
    path('first-screening/', FirstScreeningList.as_view(), name='first_screening'),
    path('first-screening/<int:pk>/', FirstScreeningDetail.as_view(), name = "screening_detail"),
    path('first-screening-modify/<int:pk>/', record_officer_modify, name='modify-screening')
]