from django.urls import path
from .views import TailorApplicationView

app_name = 'head'

urlpatterns = [
    path('tailor/', TailorApplicationView.as_view(), name='tailor-resume'),
]