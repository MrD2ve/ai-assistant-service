from django.db import models
from django.contrib.auth.models import User


class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resumes')
    title = models.CharField(max_length=255, default="My Base Resume")
    raw_text = models.TextField(help_text="Сюда вставляется исходный текст резюме")
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
    vacancy_description = models.TextField(help_text="Текст вакансии, под которую адаптируем")

    # Результаты от ИИ
    tailored_resume_text = models.TextField(blank=True, null=True, help_text="Адаптированный текст резюме")
    cover_letter = models.TextField(blank=True, null=True, help_text="Сгенерированное сопроводительное письмо")
    missing_keywords = models.JSONField(blank=True, null=True, help_text="Список ключевых слов, которых не хватало")

    # Статус для Celery (асинхронности)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    error_message = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Application for {self.resume.user.username} - {self.created_at.date()}"