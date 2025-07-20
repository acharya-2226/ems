from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Subject, Student, AttendanceRecord
from datetime import date


class AttendanceModelTests(TestCase):

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='student1', password='pass')
        self.subject = Subject.objects.create(name='Math', code='MTH101')
        self.student = Student.objects.create(user=self.user, roll_number='12345')

    def test_attendance_record_creation(self):
        attendance = AttendanceRecord.objects.create(
            student=self.student,
            subject=self.subject,
            date=date.today(),
            status='Present'
        )
        self.assertEqual(str(attendance), f"{self.student} - {self.subject.code} - {date.today()} - Present")
