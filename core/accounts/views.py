from django.urls import reverse_lazy
from django.views.generic import FormView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import SignInForm, SignUpForm
from django.shortcuts import redirect
from django.http import HttpResponse
from time import sleep 

User = get_user_model()

from .forms import SignInForm


class SignInView(FormView):
    template_name = "accounts/sign_in.html"
    form_class = SignInForm
    success_url = reverse_lazy("todo:list_task")

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        password = form.cleaned_data["password"]
        email = str(email)

        user = authenticate(request=self.request, email=email, password=password)

        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:  # Correctly using "else"
            messages.error(self.request, "This user does not exist.")
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, "The entered captcha does not match.")
        return super().form_invalid(form)


class SignUpView(FormView):
    template_name = "accounts/sign_up.html"
    form_class = SignUpForm
    success_url = reverse_lazy("accounts:sign_in")

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        password = form.cleaned_data["password"]
        confirm_password = form.cleaned_data["confirm_password"]

        if not User.objects.filter(email=email).exists():
            if password == confirm_password:
                User.objects.create_user(email=email, password=password)
                return super().form_valid(form)
            else:
                messages.error(
                    self.request,
                    "New password and confirm password do not match.",
                )
        else:
            messages.error(self.request, "This username already exists.")


class LogoutView(LoginRequiredMixin, FormView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("accounts:sign_in")

