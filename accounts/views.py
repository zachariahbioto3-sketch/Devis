from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User


def home(request):
    client_steps = [
        {"title": "Post your project", "desc": "Describe what you need, set your budget and deadline."},
        {"title": "Review proposals",  "desc": "Developers bid on your project. Compare profiles and quotes."},
        {"title": "Track milestones",  "desc": "Work is broken into milestones you approve one by one."},
        {"title": "Pay via M-Pesa",    "desc": "Release payment only when you are satisfied with the work."},
    ]
    dev_steps = [
        {"title": "Build your profile", "desc": "Add skills, certifications and portfolio projects."},
        {"title": "Browse and bid",     "desc": "Apply to projects that match your stack and rate."},
        {"title": "Deliver milestones", "desc": "Submit work per milestone and get client approval."},
        {"title": "Get paid instantly", "desc": "Receive M-Pesa payments directly to your phone."},
    ]
    return render(request, "home.html", {"client_steps": client_steps, "dev_steps": dev_steps})


def register_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        username  = request.POST.get("username", "").strip()
        email     = request.POST.get("email", "").strip().lower()
        password1 = request.POST.get("password1", "")
        password2 = request.POST.get("password2", "")
        role      = request.POST.get("role", "")

        if not all([username, email, password1, password2, role]):
            messages.error(request, "All fields are required.")
            return render(request, "accounts/register.html", {"form_data": request.POST})

        if role not in ("client", "developer"):
            messages.error(request, "Please select a valid role.")
            return render(request, "accounts/register.html", {"form_data": request.POST})

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return render(request, "accounts/register.html", {"form_data": request.POST})

        if len(password1) < 8:
            messages.error(request, "Password must be at least 8 characters.")
            return render(request, "accounts/register.html", {"form_data": request.POST})

        if User.objects.filter(email=email).exists():
            messages.error(request, "An account with that email already exists.")
            return render(request, "accounts/register.html", {"form_data": request.POST})

        if User.objects.filter(username=username).exists():
            messages.error(request, "That username is already taken.")
            return render(request, "accounts/register.html", {"form_data": request.POST})

        user = User.objects.create_user(username=username, email=email, password=password1)
        user.role = role
        user.save()

        login(request, user, backend="django.contrib.auth.backends.ModelBackend")
        messages.success(request, f"Welcome to DevMarket, {user.username}!")
        return redirect("dashboard")

    return render(request, "accounts/register.html")


def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        email    = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")
        next_url = request.POST.get("next", "")

        if not email or not password:
            messages.error(request, "Email and password are required.")
            return render(request, "accounts/login.html", {"next": next_url})

        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            return redirect(next_url or "dashboard")
        else:
            messages.error(request, "Invalid email or password.")
            return render(request, "accounts/login.html", {"email": email, "next": next_url})

    return render(request, "accounts/login.html", {"next": request.GET.get("next", "")})


def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("home")


@login_required
def dashboard_redirect(request):
    if request.user.is_client:
        return redirect("client_dashboard")
    elif request.user.is_developer:
        return redirect("dev_dashboard")
    return redirect("home")


def pricing(request):
    return render(request, "accounts/pricing.html")
