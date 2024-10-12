from django.urls import include, path
from . import views

urlpatterns = [path("register/", views.UserRegistrationView.as_view(), name="register")]
