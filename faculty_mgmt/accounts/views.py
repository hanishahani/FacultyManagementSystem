from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from .models import User
from django.contrib.auth.decorators import login_required

# Dashboard view
@login_required  # Ensures the user is logged in
def dashboard(request):
    return render(request, 'accounts/dashboard.html')

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user = User.objects.get(email=email)
                if user.check_password(password):
                    login(request, user)
                    return redirect('dashboard')  # Redirect to dashboard after login
                else:
                    form.add_error(None, "Invalid credentials")
            except User.DoesNotExist:
                form.add_error(None, "Invalid credentials")
    else:
        form = LoginForm()
    return render(request, "accounts/login.html", {"form": form})

from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout
