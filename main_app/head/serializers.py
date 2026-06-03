from rest_framework import serializers
from .models import TailoredApplication, Resume


class TailoredApplicationSerializer(serializers.ModelSerializer):
    # Мы передаем только ID резюме и текст вакансии
    resume_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = TailoredApplication
        fields = ['id', 'resume_id', 'vacancy_description', 'tailored_resume_text', 'cover_letter', 'missing_keywords',
                  'status']
        read_only_fields = ['tailored_resume_text', 'cover_letter', 'missing_keywords', 'status']

    def create(self, validated_data):
        resume_id = validated_data.pop('resume_id')
        # Проверяем, существует ли такое резюме в базе
        resume = Resume.objects.get(id=resume_id)

        # Создаем запись в базе со статусом PENDING
        application = TailoredApplication.objects.create(resume=resume, **validated_data)
        return application