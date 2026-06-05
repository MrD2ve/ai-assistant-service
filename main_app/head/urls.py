from django.urls import path
from .views import ApplicationView, index_view, TaskStatusView

app_name = 'head'

urlpatterns = [
    path('', index_view, name='index'),
    path('tailor/', ApplicationView.as_view()),
    path('tailor/status/<int:pk>/', TaskStatusView.as_view(), name='task-status'),
]