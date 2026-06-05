from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from .models import Application
from .serializers import ApplicationSerializer
from .tasks import run_ai_tailor_task


def index_view(request):
    return render(request, 'index.html')


# 1. This endpoint only accepts data and starts Celery.
class ApplicationView(APIView):
    def post(self, request):
        serializer = ApplicationSerializer(data=request.data)
        if serializer.is_valid():
            # Create a record with the status PENDING
            application = serializer.save(status='PENDING')

            # We launch the task asynchronously via .delay()
            run_ai_tailor_task.delay(application.id)

            # Instantly return the ID of the created task
            return Response(ApplicationSerializer(application).data, status=status.HTTP_201_CREATED)

        print("Validation failed:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 2. A new endpoint that the frontend will poll (Polling)
class TaskStatusView(APIView):
    def get(self, request, pk):
        try:
            application = Application.objects.get(pk=pk)
            # Return the current status of the record (PENDING, SUCCESS, or FAILED)
            return Response(ApplicationSerializer(application).data, status=status.HTTP_200_OK)
        except Application.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)