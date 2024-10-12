from django.shortcuts import render
from django.views.generic import FormView
from .forms import userRegistrationForm
from django.contrib.auth import login
from django.urls import reverse_lazy


class UserRegistrationView(FormView):
    form_class = userRegistrationForm
    template_name = "accounts/user_registration.html"
    success_url = reverse_lazy("register")

    def form_valid(self, form):
        user = form.save()
        login(user)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page"] = "User Registration"
        return context
