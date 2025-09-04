from django import forms
from .models import EmailAccount

class EmailAccountForm(forms.ModelForm):
    class Meta:
        model = EmailAccount
        fields = ["company_name", "smtp_host", "smtp_port", "use_tls", "email_address", "email_password"]
        widgets = {
            "email_password": forms.PasswordInput(),
        }
