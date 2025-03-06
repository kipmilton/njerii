from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

class Subject(models.Model):
    name = models.CharField(max_length=100, default='Chemistry')  
    description = models.TextField(default='CBC')  
    image = models.ImageField(upload_to='subjects/', blank=True, null=True)

    def __str__(self):
        return self.name
    

class Assignment(models.Model):
    title = models.CharField(max_length=255, default='Our Subjects')
    description = models.TextField(default='CBC')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)  
    due_date = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)  # Auto updates on save
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Completed', 'Completed')], default='Pending')
    file = models.FileField(upload_to='assignments/', blank=True, null=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="questions")
    text = models.TextField()

    def __str__(self):
        return f"Question for {self.subject.name}"

class Submission(models.Model):
    """Model for students' assignment and question submissions."""
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, null=True, blank=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to='submissions/', blank=True, null=True)  # Allow blank submissions
    status = models.CharField(max_length=20, choices=[('Not Attempted', 'Not Attempted'), ('Attempted', 'Attempted')], default='Not Attempted')
    grade = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        if self.assignment:
            return f"{self.student.username} - {self.assignment.title}"
        elif self.question:
            return f"{self.student.username} - {self.question.subject.name}"

