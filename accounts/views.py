from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required


def home(request):
    client_steps = [
        {"title": "Post your project", "desc": "Describe what you need, set your budget and deadline."},
        {"title": "Review proposals", "desc": "Developers bid on your project. Compare profiles and quotes."},
        {"title": "Track milestones", "desc": "Work is broken into milestones you approve one by one."},
        {"title": "Pay via M-Pesa", "desc": "Release payment only when you are satisfied with the work."},
    ]
    dev_steps = [
        {"title": "Build your profile", "desc": "Add skills, certifications and portfolio projects."},
        {"title": "Browse and bid", "desc": "Apply to projects that match your stack and rate."},
        {"title": "Deliver milestones", "desc": "Submit work per milestone and get client approval."},
        {"title": "Get paid instantly", "desc": "Receive M-Pesa payments directly to your phone."},
    ]
    return render(request, "home.html", {
        "client_steps": client_steps,
        "dev_steps": dev_steps,
    })


def login_view(request):
    return render(request, "accounts/login.html")


def logout_view(request):
    logout(request)
    return redirect("home")


def register(request):
    return render(request, "accounts/register.html")


@login_required
def dashboard_redirect(request):
    if request.user.is_client:
        return redirect("client_dashboard")
    elif request.user.is_developer:
        return redirect("dev_dashboard")
    return redirect("home")


def pricing(request):
    return render(request, "accounts/pricing.html")
