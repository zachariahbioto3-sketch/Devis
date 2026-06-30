from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count
from developers.models import DeveloperProfile, DeveloperSkill
from projects.models import Bid
from contracts.models import Contract, Milestone, Deliverable


def get_or_create_profile(user):
    profile, _ = DeveloperProfile.objects.get_or_create(
        user=user,
        defaults={"slug": user.username}
    )
    return profile


@login_required
def dashboard(request):
    profile = get_or_create_profile(request.user)

    all_bids      = Bid.objects.filter(developer=profile).select_related("project")
    pending_bids  = all_bids.filter(status="pending")
    accepted_bids = all_bids.filter(status="accepted")

    active_contracts = Contract.objects.filter(
        bid__developer=profile, status="active"
    ).select_related("project", "bid").prefetch_related("milestones")

    completed_contracts = Contract.objects.filter(
        bid__developer=profile, status="completed"
    )

    pending_milestones = Milestone.objects.filter(
        contract__bid__developer=profile,
        status="in_progress"
    ).select_related("contract__project")[:5]

    total_earned = Milestone.objects.filter(
        contract__bid__developer=profile,
        status="paid"
    ).aggregate(total=Sum("amount"))["total"] or 0

    skills = DeveloperSkill.objects.filter(
        developer=profile
    ).select_related("skill")[:8]

    try:
        subscription = profile.subscription
    except Exception:
        subscription = None

    ctx = {
        "profile":            profile,
        "pending_bids":       pending_bids,
        "pending_bids_count": pending_bids.count(),
        "active_contracts":   active_contracts,
        "active_count":       active_contracts.count(),
        "completed_count":    completed_contracts.count(),
        "pending_milestones": pending_milestones,
        "total_earned":       total_earned,
        "skills":             skills,
        "subscription":       subscription,
        "total_bids":         all_bids.count(),
    }
    return render(request, "developers/dashboard.html", ctx)


@login_required
def my_contracts(request):
    profile = get_or_create_profile(request.user)
    contracts = Contract.objects.filter(
        bid__developer=profile
    ).select_related("project", "bid").prefetch_related("milestones").order_by("-created_at")
    return render(request, "developers/contracts.html", {"contracts": contracts})


@login_required
def contract_detail(request, pk):
    profile  = get_or_create_profile(request.user)
    contract = get_object_or_404(Contract, pk=pk, bid__developer=profile)
    milestones = contract.milestones.all().prefetch_related("deliverables")
    return render(request, "developers/contract_detail.html", {
        "contract":   contract,
        "milestones": milestones,
    })


@login_required
def submit_deliverable(request, pk):
    profile   = get_or_create_profile(request.user)
    milestone = get_object_or_404(
        Milestone, pk=pk, contract__bid__developer=profile
    )

    if milestone.status not in ["pending", "in_progress"]:
        messages.error(request, "This milestone cannot be submitted right now.")
        return redirect("dev_contract_detail", pk=milestone.contract.pk)

    if request.method == "POST":
        description = request.POST.get("description", "").strip()
        file_url    = request.POST.get("file_url", "").strip()
        file        = request.FILES.get("file")

        if not description:
            messages.error(request, "Please describe what you have delivered.")
        else:
            Deliverable.objects.create(
                milestone=milestone,
                description=description,
                file_url=file_url,
                file=file if file else None,
            )
            milestone.status = "submitted"
            milestone.save()
            messages.success(request, f'{milestone.title}" submitted for client review.')
            return redirect("dev_contract_detail", pk=milestone.contract.pk)

    return render(request, "developers/submit_deliverable.html", {
        "milestone": milestone,
    })


@login_required
def my_bids(request):
    profile = get_or_create_profile(request.user)
    bids = Bid.objects.filter(developer=profile).select_related("project").order_by("-created_at")
    return render(request, "developers/bids.html", {"bids": bids})


@login_required
def withdraw_bid(request, pk):
    profile = get_or_create_profile(request.user)
    bid = get_object_or_404(Bid, pk=pk, developer=profile, status="pending")
    if request.method == "POST":
        bid.status = "withdrawn"
        bid.save()
        messages.success(request, "Bid withdrawn.")
    return redirect("dev_bids")


@login_required
def earnings(request):
    profile = get_or_create_profile(request.user)
    paid_milestones = Milestone.objects.filter(
        contract__bid__developer=profile, status="paid"
    ).select_related("contract__project").order_by("-contract__created_at")
    total = paid_milestones.aggregate(total=Sum("amount"))["total"] or 0
    return render(request, "developers/earnings.html", {
        "paid_milestones": paid_milestones,
        "total":           total,
    })


@login_required
def profile(request):
    dev_profile = get_or_create_profile(request.user)
    return render(request, "developers/profile.html", {"dev_profile": dev_profile})


@login_required
def portfolio(request):
    dev_profile = get_or_create_profile(request.user)
    projects = dev_profile.portfolio_projects.all()
    return render(request, "developers/portfolio.html", {
        "dev_profile": dev_profile,
        "projects":    projects,
    })


@login_required
def add_portfolio_project(request):
    return render(request, "developers/add_portfolio.html")


@login_required
def delete_portfolio_project(request, pk):
    return redirect("dev_portfolio")


@login_required
def manage_skills(request):
    dev_profile = get_or_create_profile(request.user)
    from developers.models import Skill
    all_skills = Skill.objects.all()
    dev_skills = DeveloperSkill.objects.filter(developer=dev_profile).select_related("skill")
    return render(request, "developers/skills.html", {
        "dev_profile": dev_profile,
        "all_skills":  all_skills,
        "dev_skills":  dev_skills,
    })


@login_required
def manage_certifications(request):
    return render(request, "developers/certifications.html")


@login_required
def metrics(request):
    return render(request, "developers/metrics.html")


@login_required
def subscription(request):
    dev_profile = get_or_create_profile(request.user)
    try:
        sub = dev_profile.subscription
    except Exception:
        sub = None
    return render(request, "developers/subscription.html", {"subscription": sub})


@login_required
def my_products(request):
    dev_profile = get_or_create_profile(request.user)
    from store.models import SoftwareProduct
    products = SoftwareProduct.objects.filter(developer=dev_profile)
    return render(request, "developers/products.html", {"products": products})


@login_required
def upload_product(request):
    return render(request, "developers/upload_product.html")


@login_required
def edit_product(request, pk):
    return render(request, "developers/edit_product.html")


@login_required
def delete_product(request, pk):
    return redirect("dev_products")


def public_profile(request, slug):
    dev_profile = get_object_or_404(DeveloperProfile, slug=slug)
    return render(request, "developers/public_profile.html", {"dev_profile": dev_profile})
