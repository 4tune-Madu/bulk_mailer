"""
URL configuration for bulk_mailer project.
"""

from django.contrib import admin
from django.urls import path, include
from mailer.views import home_view, send_email_view, add_email_account, signup_view, login_view
from django.contrib.auth import views as auth_views


urlpatterns = [
    # Home
    path('', home_view, name='home'),

    # Admin
    path('admin/', admin.site.urls),

    # Email sending routes
    path("send-email/", send_email_view, name="send_email"),
    path("add-account/", add_email_account, name="add_email_account"),

    # Authentication routes
    path("signup/", signup_view, name="signup"),
    path("login/", login_view, name="login"),

    # Optional: include Django built-in auth URLs for password reset/change, etc.
    path("accounts/", include("django.contrib.auth.urls")),
    
    # Logout view
    path("logout/", auth_views.LogoutView.as_view(next_page="login"), name="logout"),

    # User Profile
    path("profile/", include("user_profile.urls")),
]

