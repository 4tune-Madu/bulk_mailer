from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from .forms import SignUpForm, EmailAccountForm
from .models import EmailAccount

# ----------------------------
# Signup view
# ----------------------------
from django.shortcuts import render, redirect
from django.contrib.auth import login, get_backends
from .forms import SignUpForm

def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()

            # ✅ explicitly set the backend
            backend = get_backends()[0]
            user.backend = f"{backend.__module__}.{backend.__class__.__name__}"

            login(request, user)  # log in immediately
            return redirect("send_email")
    else:
        form = SignUpForm()
    return render(request, "signup.html", {"form": form})


# ----------------------------
# Login view
# ----------------------------
# mailer/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib import messages

User = get_user_model()

def login_view(request):
    if request.method == "POST":
        identifier = request.POST.get("username")  # could be username or email
        password = request.POST.get("password")

        user = None
        # First, check if the identifier looks like an email
        if "@" in identifier:
            try:
                user_obj = User.objects.get(email__iexact=identifier)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                user = None
        else:
            # Try normal username authentication
            user = authenticate(request, username=identifier, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")  # redirect to homepage
        else:
            messages.error(request, "Invalid username or email, or password.")

    return render(request, "mailer/login.html")


# ----------------------------
# Logout view
# ----------------------------
@login_required
def logout_view(request):
    logout(request)
    return redirect("login")

# ----------------------------
# Add Email Account
# ----------------------------
# mailer/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import EmailAccountForm
from .models import EmailAccount
from user_profile.utils import detect_smtp_settings   # <-- import from user_profile

@login_required
def add_email_account(request):
    if request.method == "POST":
        form = EmailAccountForm(request.POST)
        if form.is_valid():
            email_account = form.save(commit=False)
            email_account.user = request.user

            # Auto detect SMTP if empty
            if not email_account.smtp_server or not email_account.smtp_port:
                email_account.smtp_server, email_account.smtp_port = detect_smtp_settings(email_account.email)

            email_account.save()
            messages.success(request, "✅ Email account added successfully!")
            return redirect("profile")
        else:
            messages.error(request, "❌ Please correct the errors in the form.")
    else:
        form = EmailAccountForm()
    
    return render(request, "mailer/add_account.html", {"form": form})


# ----------------------------
# Send Email view
# ----------------------------
# mailer/views.py (relevant parts)
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.core.mail import EmailMessage
from .models import EmailAccount
from .utils import send_email_via_account

@login_required
def send_email_view(request):
    context = {}
    user_accounts = EmailAccount.objects.filter(user=request.user)
    context["user_accounts"] = user_accounts

    if request.method == "POST":
        subject = (request.POST.get("subject") or "").strip()
        message = (request.POST.get("message") or "").strip()
        # IMPORTANT: the template must submit hidden <input name="recipients" value="..."> for every recipient
        recipients = [r.strip() for r in request.POST.getlist("recipients") if r.strip()]
        sender_account_id = request.POST.get("sender_email")

        # Basic validation / helpful errors
        if not user_accounts.exists():
            context["error"] = "You have no email accounts configured."
            return render(request, "mailer/send_email.html", context)

        if not sender_account_id:
            context["error"] = "Please select a sending account."
            return render(request, "mailer/send_email.html", context)

        if not subject or not message:
            context["error"] = "Subject and message cannot be empty."
            return render(request, "mailer/send_email.html", context)

        if not recipients:
            context["error"] = "Please add at least one recipient."
            return render(request, "mailer/send_email.html", context)

        account = get_object_or_404(EmailAccount, id=sender_account_id, user=request.user)

        try:
            attachments = request.FILES.getlist("attachments")
            sent_count = send_email_via_account(
                account=account,
                subject=subject,
                body=message,
                recipients=recipients,
                attachments=attachments,
            )
            if sent_count:
                context["success"] = f"✅ Email sent to {len(recipients)} recipient(s)."
            else:
                context["error"] = "Email not sent — SMTP did not accept any recipients."
        except Exception as e:
            context["error"] = f"❌ Failed to send email: {e}"

    return render(request, "mailer/send_email.html", context)

# ----------------------------
# Home view
# ----------------------------

from django.shortcuts import render

def home_view(request):
    return render(request, "mailer/home.html")
