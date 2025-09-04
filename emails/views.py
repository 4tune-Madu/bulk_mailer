from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.core.mail import EmailMessage, get_connection
from .forms import EmailAccountForm
from .models import EmailAccount

def add_email_account(request):
    if request.method == "POST":
        form = EmailAccountForm(request.POST)
        if form.is_valid():
            email_account = form.save(commit=False)
            email_account.user = request.user  # attach to logged-in user
            email_account.save()
            return redirect("send_email")
    else:
        form = EmailAccountForm()
    return render(request, "emails/add_account.html", {"form": form})


from django.core.mail import EmailMessage
from .models import EmailAccount

from django.shortcuts import render, get_object_or_404
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required
from .models import EmailAccount

@login_required
def send_email_view(request):
    context = {}

    # Fetch all email accounts for the logged-in user
    user_accounts = EmailAccount.objects.filter(user=request.user)
    context["user_accounts"] = user_accounts

    if request.method == "POST":
        subject = request.POST.get("subject")
        message = request.POST.get("message")
        recipients = request.POST.getlist("recipients")  # collect all recipient inputs
        sender_account_id = request.POST.get("sender_email")

        if not recipients:
            context["error"] = "Please add at least one recipient."
            return render(request, "emails/send_email.html", context)

        # Get the selected sending email account
        account = get_object_or_404(EmailAccount, id=sender_account_id, user=request.user)

        try:
            email = EmailMessage(
                subject=subject,
                body=message,
                from_email=account.email,  # selected sending email
                to=recipients,              # list of recipients
            )
            email.send()
            context["success"] = "✅ Email sent successfully!"
        except Exception as e:
            context["error"] = f"❌ Failed to send email: {e}"

    return render(request, "emails/send_email.html", context)



