from django.test import TestCase

from ..models import Task
from accounts.models import CustomUser


class TestTask(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email="test@test.com",
            password="a123"
        )

    def test_task_valid_data(self):
        task = Task.objects.create(
            user=self.user,
            title="test",
        )

        self.assertIsNotNone(task)

    
