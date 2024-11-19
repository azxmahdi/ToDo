from django.test import TestCase

from todo.forms import TaskForm


class TestTask(TestCase):
    def test_form_task_valid(self):
        data = {
            "title": "test"
        }

        form = TaskForm(data=data)
        self.assertTrue(form.is_valid())

    def test_form_invalid(self):
        form_data = {
            'title': '',
            
        }
        form = TaskForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
        
