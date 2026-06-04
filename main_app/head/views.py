from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Application
from .serializers import ApplicationSerializer
from .services import generate_tailored_resume  # Твоя функция запроса к ИИ
from django.shortcuts import render

# Имя должно строго совпадать, маленькими буквами, через нижнее подчеркивание
def index_view(request):
    return render(request, 'index.html')

class ApplicationView(APIView):

    def post(self, request):
        serializer = ApplicationSerializer(data=request.data)

        if serializer.is_valid():
            # 1. Создаем запись в БД со статусом PENDING
            application = serializer.save(status='PENDING')

            # 2. Вызываем ИИ, передавая ТЕКСТ резюме и ТЕКСТ вакансии напрямую
            ai_response = generate_tailored_resume(
                resume_text=application.resume_text,
                vacancy_text=application.vacancy_description
            )

            # 3. Проверяем на ошибки OpenRouter
            if "Error:" in ai_response:
                application.status = 'FAILED'
                application.save()
                return Response({
                    "status": "FAILED",
                    "error_details": ai_response
                }, status=status.HTTP_400_BAD_REQUEST)

            # 4. Парсим ответ ИИ по нашему маркеру [SPLIT]
            if "[SPLIT]" in ai_response:
                parts = ai_response.split("[SPLIT]")
                application.cover_letter = parts[0].strip()
                application.missing_keywords = parts[1].strip()
            else:
                application.cover_letter = ai_response
                application.missing_keywords = "Could not split custom fields automatically."

            # 5. Меняем статус на SUCCESS и сохраняем
            application.status = 'SUCCESS'
            application.save()

            # Возвращаем обновленные данные фронтенду
            return Response(ApplicationSerializer(application).data, status=status.HTTP_201_CREATED)

        else:
            # Если фронтенд что-то недослал — выводим лог в консоль
            print("Serializer validation failed:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)