from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from .models import Project, Bid
from .forms import ProjectForm
from clients.models import ClientProfile
from developers.models import Skill


def browse_projects(request):
    projects = Project.objects.filter(status="open").annotate(
        bid_count=Count("bids")
    ).select_related("client__user").prefetch_related("skills_required").order_by("-created_at")

    # Filters
    category = request.GET.get("category", "")
    search   = request.GET.get("q", "")
    budget   = request.GET.get("budget", "")

    if category:
        projects = projects.filter(category=category)

    if search:
        projects = projects.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search) |
            Q(skills_required__name__icontains=search)
        ).distinct()

    if budget == "low":
        projects = projects.filter(budget_max__lte=20000)
    elif budget == "mid":
        projects = projects.filter(budget_min__gte=20000, budget_max__lte=100000)
    elif budget == "high":
        projects = projects.filter(budget_min__gte=100000)

    categories = Project.CATEGORY_CHOICES
    total = projects.count()

    budget_options = [
        ("",     "Any budget"),
        ("low",  "Under KES 20,000"),
        ("mid",  "KES 20,000 – 100,000"),
        ("high", "Over KES 100,000"),
    ]
    return render(request, "projects/browse.html", {
        "projects":       projects,
        "categories":     categories,
        "total":          total,
        "category":       category,
        "search":         search,
        "budget":         budget,
        "budget_options": budget_options,
    })


def project_detail(request, pk):
    project = get_object_or_404(
        Project.objects.select_related("client__user")
                       .prefetch_related("skills_required", "bids__developer__user"),
        pk=pk
    )
    user_bid = None
    if request.user.is_authenticated and hasattr(request.user, "dev_profile"):
        user_bid = project.bids.filter(developer=request.user.dev_profile).first()

    return render(request, "projects/detail.html", {
        "project":  project,
        "user_bid": user_bid,
        "bid_count": project.bids.count(),
    })


@login_required
def place_bid(request, pk):
    project = get_object_or_404(Project, pk=pk, status="open")

    if not request.user.is_developer:
        messages.error(request, "Only developers can place bids.")
        return redirect("project_detail", pk=pk)

    profile = request.user.dev_profile
    existing = Bid.objects.filter(project=project, developer=profile).first()
    if existing:
        messages.warning(request, "You have already bid on this project.")
        return redirect("project_detail", pk=pk)

    if request.method == "POST":
        amount       = request.POST.get("amount")
        timeline     = request.POST.get("timeline_days")
        cover_letter = request.POST.get("cover_letter", "").strip()

        if not all([amount, timeline, cover_letter]):
            messages.error(request, "All fields are required.")
        elif len(cover_letter) < 50:
            messages.error(request, "Cover letter must be at least 50 characters.")
        else:
            Bid.objects.create(
                project=project,
                developer=profile,
                amount=amount,
                timeline_days=timeline,
                cover_letter=cover_letter,
            )
            return redirect("project_detail", pk=pk)

    return render(request, "projects/place_bid.html", {"project": project})


def search_projects(request):
    return redirect(f"/projects/?q={request.GET.get("q", "")}")
