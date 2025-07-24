from django import forms
from django.utils import timezone
from .models import AttendanceRecord, Student
from timetable.models import Timetable
from core.models import Subject, Teacher, Room, TimeSlot


class BulkAttendanceForm(forms.Form):
    date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date', 
            'class': 'form-control',
            'max': timezone.now().date().isoformat()
        }),
        label="Attendance Date",
        initial=timezone.now().date()
    )
    subject = forms.ModelChoiceField(
        queryset=Subject.objects.filter(is_active=True),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Subject",
        empty_label="Select a subject"
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # If user is a teacher, filter subjects they teach
        if user:
            self.fields['subject'].queryset = Subject.objects.filter(teacher=user, is_active=True)


class AttendanceReportForm(forms.Form):
    student = forms.ModelChoiceField(
        queryset=Student.objects.filter(is_active=True),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Student",
        empty_label="All Students"
    )
    subject = forms.ModelChoiceField(
        queryset=Subject.objects.filter(is_active=True),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Subject",
        empty_label="All Subjects"
    )
    start_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date', 
            'class': 'form-control'
        }),
        label="From Date"
    )
    end_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date', 
            'class': 'form-control',
            'max': timezone.now().date().isoformat()
        }),
        label="To Date"
    )
    status = forms.ChoiceField(
        choices=[('', 'All Status')] + AttendanceRecord.STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Status"
    )

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date and start_date > end_date:
            raise forms.ValidationError("Start date cannot be later than end date.")
        
        return cleaned_data


class StudentAttendanceFilterForm(forms.Form):
    subject = forms.ModelChoiceField(
        queryset=Subject.objects.filter(is_active=True),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Subject",
        empty_label="All Subjects"
    )
    start_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date', 
            'class': 'form-control'
        }),
        label="From Date"
    )
    end_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date', 
            'class': 'form-control',
            'max': timezone.now().date().isoformat()
        }),
        label="To Date"
    )
    
    def __init__(self, *args, **kwargs):
        student = kwargs.pop('student', None)
        super().__init__(*args, **kwargs)
        
        # Filter subjects for the specific student
        if student:
            self.fields['subject'].queryset = student.subjects.filter(is_active=True)