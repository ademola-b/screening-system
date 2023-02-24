import string

import random
from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save

# Create your models here.
gender_choices = [
    ('male', 'Male'),
    ('female', 'Female'),
    ('other', 'Other')
]

level_choices = [
    ('100', '100'),
    ('200', '200'),
    ('300', '300'),
    ('400', '400')
]

def random_string_gen(size=8, chars=string.digits):
    return '2022'+''.join(random.choice(chars) for _ in range(size))

def unique_application_no_generator(instance):
    new_application_no = random_string_gen()

    Klass = instance.__class__
    qs_exist = Klass.objects.filter(application_no=new_application_no).exists()
    if qs_exist:
        return unique_application_no_generator
    return new_application_no


def student_directory_path(instance, filename):
    return '{0}/{1}'.format(instance.application_no, filename)
   

class Level(models.Model):
    levelInit = models.CharField(max_length=5, choices=level_choices, default='100', unique=True)

    def __str__(self):
        return self.levelInit

class Department(models.Model):
    deptName = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.deptName 

class Student(models.Model):
    user_id = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    application_no = models.CharField(max_length=15, unique=True, blank=True)
    registration_no = models.CharField(max_length=12, unique=True, null=True, blank=True)
    profile_pix = models.ImageField(upload_to=student_directory_path)
    level_id = models.ForeignKey(Level, on_delete=models.CASCADE)
    department_id = models.ForeignKey(Department, on_delete=models.CASCADE)
    phone_no = models.CharField(max_length=11)
    address = models.TextField()
    gender = models.CharField(max_length=10, choices=gender_choices, default='other')
    dob = models.DateField(auto_now=False, auto_now_add=False)

    def __str__(self):
        return self.user_id.email

def pre_save_create_application_no(sender, instance, *args, **kwargs):
    if not instance.application_no:
        instance.application_no = unique_application_no_generator(instance)

pre_save.connect(pre_save_create_application_no, sender=Student)