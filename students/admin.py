from django.contrib import admin

from .models import *

# Register your models here.

admin_models = [
  Department, Level, Student
]

for i in admin_models:
    admin.site.register(i)