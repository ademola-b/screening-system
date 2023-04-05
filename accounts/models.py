from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.utils.translation import gettext_lazy as _

# Create your models here.

class CustomUserManager(BaseUserManager):
    "define a model manager for user model with no username field"

    def _create_user(self, email, password=None, **extra_fields):
        """create and save a user with email and password"""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)


    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')

        return self._create_user(email, password, **extra_fields)

        

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    user_type = models.CharField(max_length=30, choices=[('admin', 'Admin'),('student', 'Student'), ('record_officer','Record Officer'), ('student_affair','Student Affair Officer')], default="student")


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    object = CustomUserManager()


# class User(AbstractUser):
#     username = None
#     user_type_choices = [
#        ('student', 'student'),
#         ('record_officer', 'record_officer'),
#         ('student_affair_officer', 'student_affair_officer')
#     ]
        
#     email = models.EmailField(unique=True)
#     user_type = models.CharField(max_length=25, choices=user_type_choices, default='student')
