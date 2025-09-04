from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from mailer.models import EmailAccount
from .forms import UserProfileForm

@login_required
def profile_view(request):
    user = request.user
    email_accounts = user.mailer_email_accounts.all() #related name

    user_form = UserProfileForm(instance=user)

    if request.method == 'POST':
        # Update user profile
        if 'update_user' in request.POST:
            user_form = UserProfileForm(request.POST, instance=user)
            if user_form.is_valid():
                user_form.save()
                messages.success(request, "✅ Profile updated successfully!")
                return redirect('profile')
            else:
                messages.error(request, "❌ Please correct the errors in the profile form.")

        # Edit email account
        elif 'edit_email' in request.POST:
            account_id = request.POST.get('account_id')
            account = get_object_or_404(EmailAccount, id=account_id, user=user)

            # Update fields directly from POST
            account.email = request.POST.get('email', account.email)
            account.password = request.POST.get('password', account.password)
            account.smtp_server = request.POST.get('smtp_server', account.smtp_server)
            account.smtp_port = request.POST.get('smtp_port', account.smtp_port)

            account.save()
            messages.success(request, "✅ Email account updated successfully!")
            return redirect('profile')

        # Delete email account
        elif 'delete_email' in request.POST:
            account_id = request.POST.get('account_id')
            account = get_object_or_404(EmailAccount, id=account_id, user=user)
            account.delete()
            messages.success(request, "✅ Email account deleted successfully!")
            return redirect('profile')

    context = {
        'user_form': user_form,
        'email_accounts': email_accounts,
    }
    return render(request, 'user_profile/profile.html', context)
