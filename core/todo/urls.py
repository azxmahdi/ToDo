from django.urls import path, include
from django.views.decorators.cache import cache_page
from .views import *

app_name = "todo"

urlpatterns = [
    path("",TaskListView.as_view(), name="list_task"),
    path("create/", TaskCreateView.as_view(), name="create_task"),
    path("delete/<int:pk>/", TaskDeleteView.as_view(), name="delete_task"),
    path("edit/<int:pk>/", TaskUpdateView.as_view(), name="edit_task"),
    path(
        "toggle_task/<int:pk>/",
        ToggleTaskUpdateView.as_view(),
        name="toggle_task",
    ),
    path("api/v1/", include("todo.api.v1.urls"), name="api-v1"),
]
