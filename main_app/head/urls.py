from django.urls import path
from .views import ApplicationView, index_view

app_name = 'head'

urlpatterns = [
    path('', index_view, name='index'),
    path('tailor/', ApplicationView.as_view(), name='tailor-resume'),
]