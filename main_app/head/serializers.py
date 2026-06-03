from rest_framework import serializers
from .models import TailoredApplication, Resume


class TailoredApplicationSerializer(serializers.ModelSerializer):
    # We only transmit the resume ID and the job posting text.
    resume_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = TailoredApplication
        fields = ['id', 'resume_id', 'vacancy_description', 'tailored_resume_text', 'cover_letter', 'missing_keywords',
                  'status']
        read_only_fields = ['tailored_resume_text', 'cover_letter', 'missing_keywords', 'status']

    def create(self, validated_data):
        resume_id = validated_data.pop('resume_id')
        # We check if such a resume exists in the database.
        resume = Resume.objects.get(id=resume_id)

        # We create a record in the database with the status PENDING
        application = TailoredApplication.objects.create(resume=resume, **validated_data)
        return application