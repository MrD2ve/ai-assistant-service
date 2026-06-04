from django.db import models
from django.contrib.auth.models import User


class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resumes')
    title = models.CharField(max_length=255, default="My Base Resume")
    raw_text = models.TextField(help_text="The original text of the resume is inserted here.")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.title}"


class Application(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed'),
    ]

    # Вместо ForeignKey теперь храним чистый текст резюме
    resume_text = models.TextField()
    vacancy_description = models.TextField()

    cover_letter = models.TextField(null=True, blank=True)
    missing_keywords = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    def __summary__(self):
        return f"Application {self.id} - {self.status}"