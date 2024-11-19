from django.contrib.auth import get_user_model
from celery import shared_task

from .models import Task

User = get_user_model()

@shared_task
def delete_all_tasks():
    """
    Deletes all tasks for verified users.
    """
    verified_users = User.objects.filter(is_verified=True)
    for user in verified_users:
        # Directly delete tasks related to the user
        Task.objects.filter(user=user,is_done=True).delete() 
