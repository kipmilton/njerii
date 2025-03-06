from django import forms
from django.contrib.auth.models import User
from .models import Assignment, Question, Submission, Subject

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'description', 'image']  # Add fields as per your Subject 
        


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['subject', 'text']


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['title', 'description', 'subject', 'due_date', 'file']  # Add fields as per your Assignment model

class GradeForm(forms.ModelForm):
    """Form for grading student submissions."""
    class Meta:
        model = Submission
        fields = ['grade']

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['image']

