from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse


class Task(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=225)
    is_done = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse("todo:api-v1:task-detail", kwargs={"pk": self.pk})
