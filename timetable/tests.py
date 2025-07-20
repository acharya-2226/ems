from django.test import TestCase
from .models import Timetable
from datetime import time


class TimetableModelTest(TestCase):

    def test_timetable_creation(self):
        timetable = Timetable.objects.create(
            day='MON',
            start_time=time(9, 0),
            end_time=time(10, 0),
            subject='Physics',
            teacher='Dr. Smith',
            classroom='Room 101'
        )
        self.assertEqual(str(timetable), 'Physics (MON) 09:00:00-10:00:00')
