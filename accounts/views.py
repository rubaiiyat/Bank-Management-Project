from django.shortcuts import render, redirect
from django.views.generic import FormView
from .forms import userRegistrationForm
from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView


class UserRegistrationView(FormView):
    form_class = userRegistrationForm
    template_name = "accounts/user_registration.html"
    success_url = reverse_lazy("register")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page"] = "User Registration"
        return context


class userLogin(LoginView):
    template_name = "accounts/login.html"

    def get_success_url(self) -> str:
        return reverse_lazy("home")


def userLogout(request):
    logout(request)
    return redirect("home")
