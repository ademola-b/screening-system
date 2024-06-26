# Generated by Django 4.1.4 on 2022-12-21 03:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import students.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deptName', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('levelInit', models.CharField(choices=[('100', '100'), ('200', '200'), ('300', '300'), ('400', '400')], default='100', max_length=5, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_pix', models.FileField(upload_to=students.models.student_directory_path)),
                ('phone_no', models.CharField(max_length=11)),
                ('address', models.TextField()),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], default='other', max_length=10)),
                ('dob', models.DateField()),
                ('department_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students.department')),
                ('level_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students.level')),
                ('user_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
