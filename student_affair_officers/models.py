from django.conf import settings
from django.db import models

from students.models import Department

# Create your models here.
def avatar_directory_path(instance, filename):
    return '{0}/{1}'.format(instance.user_id.first_name, filename)

# Create your models here.
class StudentAffairOfficer(models.Model):
    user_id = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    department_id = models.OneToOneField(Department, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to=avatar_directory_path)
    phone_no = models.CharField(max_length=11)


    def __str__(self):
        return self.user_id.first_name