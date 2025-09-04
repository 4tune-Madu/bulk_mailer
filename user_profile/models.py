from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=150, blank=True)
    username = models.CharField(max_length=150, blank=True)
    registration_email = models.EmailField(blank=True)

    def __str__(self):
        return self.user.username

