from django import forms
from .models import Timetable, Teacher

class TimetableFilterForm(forms.Form):
    day = forms.ChoiceField(
        choices=[('', 'All Days')] + Timetable.DAYS_CHOICES,
        required=False,
        label="Day"
    )
    semester = forms.ChoiceField(
        choices=[('', 'All Semesters')] + [(i, f"Semester {i}") for i in range(1, 9)],
        required=False,
        label="Semester"
    )
    teacher = forms.ModelChoiceField(
        queryset=Teacher.objects.all(),
        required=False,
        empty_label="All Teachers",
        label="Teacher"
    )


class TimetableForm(forms.ModelForm):
    class Meta:
        model = Timetable
        fields = ['day', 'time_slot', 'subject', 'teacher', 'room', 'semester', 'active']
        widgets = {
            'day': forms.Select(attrs={'class': 'form-control'}),
            'time_slot': forms.Select(attrs={'class': 'form-control'}),
            'subject': forms.Select(attrs={'class': 'form-control'}),
            'teacher': forms.Select(attrs={'class': 'form-control'}),
            'room': forms.Select(attrs={'class': 'form-control'}),
            'semester': forms.NumberInput(attrs={'class': 'form-control'}),
            'active': forms.CheckboxInput(),
        }
        labels = {
            'day': 'Day of the Week',
            'time_slot': 'Time Slot',
            'subject': 'Subject',
            'teacher': 'Teacher',
            'room': 'Room',
            'semester': 'Semester',
            'active': 'Active'
        }
        help_texts = {
            'day': 'Select the day of the week for the timetable entry.',
            'time_slot': 'Select the time slot for the class.',
            'subject': 'Select the subject being taught.',
            'teacher': 'Select the teacher responsible for this class.',
            'room': 'Select the room where the class will be held.',
            'semester': 'Enter the semester number for this class.',
            'active': 'Check if this timetable entry is currently active.'
        }
        error_messages = {
            'day': {
                'required': 'Please select a day for the timetable entry.'
            },
            'time_slot': {
                'required': 'Please select a time slot for the class.'
            },
            'subject': {
                'required': 'Please select a subject for the class.'
            },
            'teacher': {
                'required': 'Please select a teacher for this class.'
            },
            'room': {
                'required': 'Please select a room for the class.'
            },
            'semester': {
                'required': 'Please enter the semester number.'
            }
}
