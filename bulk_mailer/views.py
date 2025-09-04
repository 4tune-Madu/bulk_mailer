from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth import login as auth_login
from .forms import CustomSignupForm, CustomLoginForm


# 🔹 Signup View
def custom_signup(request):
    if request.method == "POST":
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # auto login after signup
            return redirect("home")
    else:
        form = CustomSignupForm()
    return render(request, "signup.html", {"form": form})


# 🔹 Login View
def custom_login(request):
    if request.method == "POST":
        form = CustomLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect("home")
    else:
        form = CustomLoginForm()
    return render(request, "login.html", {"form": form})


# 🔹 Logout View
from django.contrib.auth.views import LogoutView as DjangoLogoutView

class CustomLogoutView(DjangoLogoutView):
    next_page = "login"

    def get(self, request, *args, **kwargs):
        """Allow GET request for logout"""
        return self.post(request, *args, **kwargs)