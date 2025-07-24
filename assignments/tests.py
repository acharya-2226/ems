from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from .models import Assignment, Submission

class AssignmentAppTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.teacher = User.objects.create_user(
            username='teacher', 
            password='pass', 
            is_staff=True
        )
        self.student = User.objects.create_user(
            username='student', 
            password='pass'
        )
        self.client = Client()
        
        self.assignment = Assignment.objects.create(
            title="Test Assignment",
            description="Test Description",
            created_by=self.teacher,
            due_date=timezone.now() + timedelta(days=7)
        )

    def test_dashboard_view(self):
        self.client.login(username='teacher', password='pass')
        response = self.client.get(reverse('assignments:dashboard_assignments'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Assignments Dashboard')

    def test_assignment_creation(self):
        self.client.login(username='teacher', password='pass')
        response = self.client.post(reverse('assignments:upload_assignments'), {
            'title': 'New Assignment',
            'description': 'New Description',
            'max_score': 100
        })
        self.assertEqual(Assignment.objects.count(), 2)

    def test_permission_for_grading(self):
        submission = Submission.objects.create(
            assignment=self.assignment,
            student=self.student
        )
        
        # Student shouldn't be able to grade
        self.client.login(username='student', password='pass')
        response = self.client.get(
            reverse('assignments:grade_submission', kwargs={'pk': submission.pk})
        )
        self.assertEqual(response.status_code, 403)
        
        # Teacher should be able to grade
        self.client.login(username='teacher', password='pass')
        response = self.client.get(
            reverse('assignments:grade_submission', kwargs={'pk': submission.pk})
        )
        self.assertEqual(response.status_code, 200)