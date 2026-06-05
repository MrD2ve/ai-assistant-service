from rest_framework import serializers
from .models import Application, Resume


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = [
            'id',
            'resume_text',
            'vacancy_description',
            'cover_letter',
            'missing_keywords',
            'status'
        ]
        # We make AI fields optional for POST requests; the backend will fill them in automatically.
        read_only_fields = ['cover_letter', 'missing_keywords', 'status']