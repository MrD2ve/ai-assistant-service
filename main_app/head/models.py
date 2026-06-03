from django.db import models
from django.contrib.auth.models import User


class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resumes')
    title = models.CharField(max_length=255, default="My Base Resume")
    raw_text = models.TextField(help_text="The original text of the resume is inserted here.")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.title}"


class TailoredApplication(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Processing'),
        ('SUCCESS', 'Completed'),
        ('FAILED', 'Failed'),
    ]

    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='applications')
    vacancy_description = models.TextField(help_text="The text of the vacancy to which we are adapting")

    # Result from AI
    tailored_resume_text = models.TextField(blank=True, null=True, help_text="Adapted resume text")
    cover_letter = models.TextField(blank=True, null=True, help_text="Generated cover letter")
    missing_keywords = models.JSONField(blank=True, null=True, help_text="List of missing keywords")

    # Status for Celery (async)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    error_message = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Application for {self.resume.user.username} - {self.created_at.date()}"