import pytest
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.urls import reverse

from ..models import Task

User = get_user_model()

@pytest.fixture
def user_obj():
    user = User.objects.create_user(
        email="test_email@gmail.com",
        password="test_password@123",
        is_verified=True
    )
    return user

@pytest.fixture
def task_obj(user_obj):
    task = Task.objects.create(
        user=user_obj,
        title="test_title",
        is_done=False
    )
    return task


@pytest.mark.django_db()
class TestTaskAPI:
    client = APIClient()

    def test_create_task_with_valid_data(self, user_obj):
        url = reverse('todo:api-v1:task-list')
        data = {'title': 'Test Task', 'is_done': False}
        self.client.force_login(user=user_obj)
        response = self.client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['title'] == 'Test Task'

    def test_create_task_with_invalid_data(self, user_obj):
        url = reverse('todo:api-v1:task-list')
        data = {'title': ''}
        self.client.force_login(user_obj)
        response = self.client.post(url, data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_get_task_list(self, user_obj, task_obj):
        url = reverse('todo:api-v1:task-list')
        self.client.force_login(user_obj)
        response = self.client.get(url, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) > 0 

    def test_update_task(self, user_obj, task_obj):
        url = reverse('todo:api-v1:task-detail', kwargs={'pk': task_obj.id})
        self.client.force_login(user_obj)
        data = {'title': 'test_update_title'}
        response = self.client.put(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        
        task_obj.refresh_from_db()
        assert task_obj.title == 'test_update_title'
    
    def test_delete_task(self, user_obj, task_obj):
        url = reverse('todo:api-v1:task-detail', kwargs={'pk': task_obj.id})
        self.client.force_login(user_obj)
        response = self.client.delete(url, format='json')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Task.objects.filter(id=task_obj.id).count() == 0
