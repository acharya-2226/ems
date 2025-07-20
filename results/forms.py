from django import forms
from .models import Result


class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = '__all__'
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'subject': forms.Select(attrs={'class': 'form-control'}),
            'marks_obtained': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Marks Obtained'}),
            'total_marks': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Total Marks'}),
            'grade': forms.Select(attrs={'class': 'form-control'}),
            'semester': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Semester'}),
            'year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Year'}),
            'published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'student': 'Student',
            'subject': 'Subject',
            'marks_obtained': 'Marks Obtained',
            'total_marks': 'Total Marks',
            'grade': 'Grade',
            'semester': 'Semester',
            'year': 'Year',
            'published': 'Published',
        }
        help_texts = {
            'marks_obtained': 'Enter the marks obtained by the student.',
            'total_marks': 'Enter the total marks for the subject.',
            'grade': 'Select the grade based on marks obtained.',
            'semester': 'Enter the semester number.',
            'year': 'Enter the academic year.',
            'published': 'Check to make results visible to students.',
        }
        error_messages = {
            'marks_obtained': {
                'required': 'Marks obtained is required.',
                'invalid': 'Enter a valid number for marks obtained.'
            },
            'total_marks': {
                'required': 'Total marks is required.',
                'invalid': 'Enter a valid number for total marks.'
            },
            'grade': {
                'required': 'Grade is required.'
            },
            'semester': {
                'required': 'Semester is required.',
                'invalid': 'Enter a valid number for semester.'
            },
            'year': {
                'required': 'Year is required.',
                'invalid': 'Enter a valid number for year.'
            }
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['student'].empty_label = "Select Student"
        self.fields['subject'].empty_label = "Select Subject"
        self.fields['grade'].empty_label = "Select Grade"

    def clean(self):
        cleaned_data = super().clean()
        marks_obtained = cleaned_data.get('marks_obtained')
        total_marks = cleaned_data.get('total_marks')

        if marks_obtained is not None and total_marks is not None:
            if marks_obtained < 0 or total_marks <= 0:
                raise forms.ValidationError("Marks obtained must be non-negative and total marks must be positive.")
            if marks_obtained > total_marks:
                raise forms.ValidationError("Marks obtained cannot exceed total marks.")

        return cleaned_data