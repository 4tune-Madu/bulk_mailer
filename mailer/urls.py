from django.urls import path
from mailer.views import add_account
from django.contrib.auth import views as auth_views
from .views import CustomAuthenticationForm

urlpatterns = [
    path("add-account/", add_email_account, name="add_email_account"),
    path("login/", auth_views.LoginView.as_view(
        template_name="login.html",
        authentication_form=CustomAuthenticationForm
    ), name="login"),
]
