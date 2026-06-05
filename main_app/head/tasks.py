from celery import shared_task
from .models import Application
from .services import generate_tailored_resume


@shared_task
def run_ai_tailor_task(application_id):
    try:
        # 1. We retrieve a record from the database
        application = Application.objects.get(id=application_id)

        # 2. Making a long query to the AI in a background Celery thread
        ai_response = generate_tailored_resume(
            resume_text=application.resume_text,
            vacancy_text=application.vacancy_description
        )

        # 3. Processing the response
        if "Error:" in ai_response:
            application.status = 'FAILED'
            application.cover_letter = ai_response
        else:
            if "[SPLIT]" in ai_response:
                parts = ai_response.split("[SPLIT]")
                application.cover_letter = parts[0].strip()
                application.missing_keywords = parts[1].strip()
            else:
                application.cover_letter = ai_response
                application.missing_keywords = "Could not split custom fields automatically."

            application.status = 'SUCCESS'

        application.save()

    except Application.DoesNotExist:
        print(f"Application with id {application_id} not found.")