from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import EmailAccount  # <-- important

# Optional: Email sending form
class EmailForm(forms.Form):
    recipients = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter comma-separated emails'}),
        label="Recipients"
    )
    subject = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'placeholder': 'Subject'}),
        label="Subject"
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Write your message here...'}),
        label="Message"
    )

# Signup form
class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

# Add Email Account form
from django import forms
from .models import EmailAccount

class EmailAccountForm(forms.ModelForm):
    class Meta:
        model = EmailAccount
        fields = ["email", "password", "smtp_server", "smtp_port"]
        widgets = {
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "password": forms.PasswordInput(attrs={"class": "form-control"}),
            "smtp_server": forms.TextInput(attrs={"class": "form-control", "placeholder": "Optional"}),
            "smtp_port": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Optional"}),
        }