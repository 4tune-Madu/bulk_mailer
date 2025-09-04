from django.db import models
from django.contrib.auth.models import User

class EmailAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="mailer_email_accounts")
    email = models.EmailField()
    password = models.CharField(max_length=255)  # app password
    smtp_server = models.CharField(max_length=255, blank=True, null=True)
    smtp_port = models.IntegerField(blank=True, null=True)

    def _str_(self):
        return f"{self.email} ({self.user.username})"