from django.shortcuts import render, redirect
from django.views.generic import FormView, TemplateView, UpdateView, View
from .forms import userRegistrationForm, userUpdateForm
from django.contrib.auth import login, logout, views
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView


class UserRegistrationView(FormView):
    form_class = userRegistrationForm
    template_name = "accounts/user_registration.html"
    success_url = reverse_lazy("accounts/profile.html")

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
        return reverse_lazy("profile")


class userProfile(View):
    template_name = "accounts/profile.html"

    def get(self, request):
        form = userUpdateForm(instance=request.user)
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = userUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("profile")
        return render(request, self.template_name, {"form": form})


def userLogout(request):
    logout(request)
    return redirect("home")
