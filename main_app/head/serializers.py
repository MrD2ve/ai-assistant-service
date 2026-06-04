from rest_framework import serializers
from .models import Application, Resume


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = [
            'id',
            'resume_text',          # Теперь валидируем текст резюме
            'vacancy_description',
            'cover_letter',
            'missing_keywords',
            'status'
        ]
        # Делаем поля ИИ необязательными при POST-запросе, бэкенд заполнит их сам
        read_only_fields = ['cover_letter', 'missing_keywords', 'status']