from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from ..models import Task

User = get_user_model()

class TaskTest(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@test.com",
            password="a123"
        )


        self.task = Task.objects.create(
            user=self.user,
            title="test title",
        )


    def test_view_status_code(self):
        self.client.force_login(self.user)
        url = reverse('todo:list_task')
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)