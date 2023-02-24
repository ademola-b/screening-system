from django.db import models

from students.models import Student

from django.core.exceptions import ValidationError



# Create your models here.


status = [
    ('pending', 'pending'),
    ('pending for record officer', 'pending for record officer'),
    ('pending for student affair', 'pending for student affair'),
    ('approved', 'approved'),
    ('rejected', 'rejected')
]

def student_directory_path(instance, filename):
    return '{0}/{1}'.format(instance.student_id.application_no, filename)


def validate_file_extension(value):
    import os
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.jpg', '.jpeg', '.png', '.pdf']
    if not ext in valid_extensions:
        raise ValidationError('File type not supported')


class FirstScreening(models.Model):
    student_id = models.OneToOneField(Student, on_delete=models.CASCADE)
    o_level = models.FileField(upload_to=student_directory_path, validators=[validate_file_extension])
    indigene_certificate = models.FileField(upload_to=student_directory_path, validators=[validate_file_extension])
    pry_certificate = models.FileField(upload_to=student_directory_path, validators=[validate_file_extension])
    ND_result = models.FileField(upload_to=student_directory_path, validators=[validate_file_extension])
    admission_letter = models.FileField(upload_to=student_directory_path, validators=[validate_file_extension])
    acceptance_fee_receipt = models.FileField(upload_to=student_directory_path, validators=[validate_file_extension])
    dateSubmitted = models.DateTimeField(auto_now_add=True)
    dateApproved = models.DateTimeField(auto_now_add=False, auto_now=True)
    status = models.CharField(max_length=30, default='Pending', choices=status)
    comment = models.TextField(max_length=1000, blank=True)

    def __str__(self):
        return '{0} - {1}'.format(self.student_id.user_id.first_name, self.student_id.application_no
    ) 


class SecondScreening(models.Model):
    student_id = models.OneToOneField(Student, on_delete=models.CASCADE)
    first_screening = models.OneToOneField(FirstScreening, on_delete=models.CASCADE, related_name='first_screening')
    acceptance_form = models.FileField(upload_to=student_directory_path, validators=[validate_file_extension])
    school_fee_receipt = models.FileField(upload_to=student_directory_path, validators=[validate_file_extension])
    medical_receipt = models.FileField(upload_to=student_directory_path, validators=[validate_file_extension])
    entrepreneur_receipt = models.FileField(upload_to=student_directory_path, validators=[validate_file_extension])
    jamb_admission_letter = models.FileField(upload_to=student_directory_path, validators=[validate_file_extension])
    jamb_original_result = models.FileField(upload_to=student_directory_path, validators=[validate_file_extension])
    attestation_letter = models.FileField(upload_to=student_directory_path, validators=[validate_file_extension])
    dateSubmitted = models.DateTimeField(auto_now_add=True)
    dateApproved = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=30, default='Pending', choices=status)
    comment = models.TextField(max_length=1000)

    def __str__(self):
        return '{0} - {1}'.format(self.student_id.user_id.first_name, self.student_id.application_no
    ) 


class Screening(models.Model):
    student_id = models.OneToOneField(Student, on_delete=models.CASCADE)
    firstScreening = models.OneToOneField(FirstScreening, on_delete=models.CASCADE)
    secondScreening = models.OneToOneField(SecondScreening, on_delete=models.CASCADE)