# emails/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("add-account/", views.add_email_account, name="add_email"),  # 👈 changed name here
]
