from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, DeleteView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Task
from .forms import TaskForm
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    fields = ["title"]
    success_url = reverse_lazy("todo:list_task")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreateView, self).form_valid(form)


class TaskListView(ListView, LoginRequiredMixin):
    model = Task
    template_name = "todo/main.html"
    context_object_name = "tasks"

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("accounts:sign_in")
        return super().dispatch(request, *args, **kwargs)


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = "task"
    success_url = reverse_lazy("todo:list_task")

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class TaskUpdateView(LoginRequiredMixin, View):
    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk, user=request.user)
        form = TaskForm(instance=task)
        return render(request, "todo/edit_task.html", {"form": form})

    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk, user=request.user)
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("todo:list_task")
        return render(request, "todo/edit_task.html", {"form": form})


class ToggleTaskUpdateView(LoginRequiredMixin, View):

    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk, user=request.user)
        task.is_done = not task.is_done
        task.save()
        return redirect("todo:list_task")


