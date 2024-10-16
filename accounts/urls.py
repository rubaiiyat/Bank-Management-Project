from django.urls import include, path
from . import views

urlpatterns = [
    path("register/", views.UserRegistrationView.as_view(), name="register"),
    path("login/", views.userLogin.as_view(), name="login"),
    path("profile/", views.userProfile.as_view(), name="profile"),
    path("logout/", views.userLogout, name="logout"),
]
