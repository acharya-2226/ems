from django.test import TestCase
from .models import Result
from datetime import date


class ResultModelTest(TestCase):

    def test_result_creation(self):
        result = Result.objects.create(
            student_name='John Doe',
            subject='Math',
            marks_obtained=85.5,
            total_marks=100,
            grade='A',
            published_date=date.today()
        )
        self.assertEqual(str(result), 'John Doe - Math')
