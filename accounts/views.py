from django.shortcuts import render
from django.views.generic import FormView
from .forms import userRegistrationForm
from django.contrib.auth import login


class UserRegistrationView(FormView):
    form_class = userRegistrationForm
    template_name = ""
    success_url = ""

    def form_valid(self, form):
        user = form.save()
        login(user)
        return super().form_valid(form)
