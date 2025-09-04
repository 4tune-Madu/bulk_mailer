from django.urls import path
from .views import profile_view
from . import views 

urlpatterns = [
    path("", views.profile_view, name="profile"), 
]
