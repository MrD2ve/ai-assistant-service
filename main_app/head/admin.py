from django.contrib import admin
from .models import Resume, TailoredApplication


admin.site.register(Resume)
admin.site.register(TailoredApplication)


# @admin.site.register(Resume)
# class ResumeAdmin(admin.ModelAdmin):
#     list_display = ['user', 'title', 'raw_text', 'created_at']
#
# @admin.site.register(TailoredApplication)
# class TailoredApplicationAdmin(admin.ModelAdmin):
#     list_display = ['resume', 'vacancy_description', 'tailored_resume_text', 'cover_letter', 'missing_keywords', 'status', 'error_message']