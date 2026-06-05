import os
from celery import Celery

# 1. Setting up default Django settings for the Celery utility
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'root.settings')

app = Celery('ai_assistant_service')

# 2. We read the configuration from settings.py with the CELERY_ prefix
app.config_from_object('django.conf:settings', namespace='CELERY')

# 3. Automatically search for tasks (tasks.py) in all registered applications (INSTALLED_APPS)
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')