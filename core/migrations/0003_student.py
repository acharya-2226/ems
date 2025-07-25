# Generated by Django 5.2.3 on 2025-07-22 05:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_teacher_department_teacher_hire_date_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('roll_number', models.CharField(blank=True, help_text='Unique roll number for the student', max_length=20, null=True, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('department', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='attendance_student_profile', to='core.department')),
                ('subjects', models.ManyToManyField(related_name='enrolled_students', to='core.subject')),
                ('user', models.OneToOneField(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='attendance_student_profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['roll_number'],
            },
        ),
    ]
