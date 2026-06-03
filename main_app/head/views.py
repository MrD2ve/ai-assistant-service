from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import TailoredApplication, Resume
from .serializers import TailoredApplicationSerializer
from .services import generate_tailored_resume  # Your service from the previous step


class TailorApplicationView(APIView):

    def post(self, request):
        serializer = TailoredApplicationSerializer(data=request.data)

        if serializer.is_valid():
            # 1. Saving the primary record to the database
            application = serializer.save()

            # 2. We take texts for sending to AI
            resume_text = application.resume.raw_text
            vacancy_text = application.vacancy_description

            # 3. Change the status to "In progress" (even though it's quick, it's necessary for logic)
            application.status = 'PENDING'
            application.save()

            # 4. Sending a request to a free AI (OpenRouter)
            ai_response = generate_tailored_resume(resume_text, vacancy_text)

            if "Error:" in ai_response:
                application.status = 'FAILED'
                application.save()
                return Response({"status": "FAILED", "error": ai_response}, status=400)

                # Split the AI answer
            if "[SPLIT]" in ai_response:
                parts = ai_response.split("[SPLIT]")
                application.cover_letter = parts[0].strip()
                application.missing_keywords = parts[1].strip()
            else:
                # Just in case the AI ignored the tag
                application.cover_letter = ai_response
                application.missing_keywords = "Failed to split the answer automatically."

            application.status = 'SUCCESS'

            application.save()

            # We return updated data to the client
            return Response(TailoredApplicationSerializer(application).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)