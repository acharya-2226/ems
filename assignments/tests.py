from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Assignment, Submission
from django.core.files.uploadedfile import SimpleUploadedFile


class AssignmentModelTests(TestCase):

    def test_assignment_creation(self):
        assignment = Assignment.objects.create(
            title="Test Assignment",
            description="Test Description",
            file=SimpleUploadedFile("testfile.pdf", b"file_content")
        )
        self.assertEqual(str(assignment), "Test Assignment")


class SubmissionModelTests(TestCase):

    def setUp(self):
        User = get_user_model()
        self.student = User.objects.create_user(username='student1', password='pass')
        self.assignment = Assignment.objects.create(
            title="Assignment 1",
            description="Description",
            file=SimpleUploadedFile("assignment.pdf", b"content")
        )

    def test_submission_creation(self):
        submission = Submission.objects.create(
            assignment=self.assignment,
            student=self.student,
            submitted_file=SimpleUploadedFile("submission.pdf", b"submission content")
        )
        self.assertEqual(str(submission), f"{self.student.username} - {self.assignment.title}")
