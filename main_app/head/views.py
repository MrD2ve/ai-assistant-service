from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import TailoredApplication, Resume
from .serializers import TailoredApplicationSerializer
from .services import generate_tailored_resume  # Твой сервис из прошлого шага


class TailorApplicationView(APIView):

    def post(self, request):
        serializer = TailoredApplicationSerializer(data=request.data)

        if serializer.is_valid():
            # 1. Сохраняем первичную запись в БД
            application = serializer.save()

            # 2. Берем тексты для отправки в ИИ
            resume_text = application.resume.raw_text
            vacancy_text = application.vacancy_description

            # 3. Меняем статус на "В процессе" (хоть это и быстро, для логики нужно)
            application.status = 'PENDING'
            application.save()

            # 4. Отправляем запрос в бесплатный ИИ (OpenRouter)
            ai_response = generate_tailored_resume(resume_text, vacancy_text)

            # 5. Сохраняем ответ ИИ в базу и меняем статус на SUCCESS
            if "Error:" in ai_response:
                application.status = 'FAILED'
                application.error_message = ai_response
            else:
                application.status = 'SUCCESS'
                application.cover_letter = ai_response
                # Пока записываем весь ответ в cover_letter, позже научим ИИ отдавать строгий JSON

            application.save()

            # Возвращаем обновленные данные клиенту
            return Response(TailoredApplicationSerializer(application).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)