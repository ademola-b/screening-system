from django.contrib import admin
from .models import  *
# Register your models here.

class CustomScreenAdmin(admin.ModelAdmin):
  list_display = ['student_id','dateSubmitted', 'dateApproved']

admin_models = [
  FirstScreening, SecondScreening
]

for i in admin_models:
    admin.site.register(i, CustomScreenAdmin)