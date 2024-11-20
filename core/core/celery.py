from os import environ
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.setting.settings_dev')

app = Celery('core')

app.conf.update(
    broker_connection_retry_on_startup=True, # Add this line 
    # ... other Celery settings 
)

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY') # Access settings directly 

# Load task modules from all registered Django apps.
app.autodiscover_tasks()
