from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Sum, Q
from projects.models import Project, Bid
from projects.forms import ProjectForm
from contracts.models import Contract, Milestone
from clients.models import ClientProfile


def get_or_create_profile(user):
    profile, _ = ClientProfile.objects.get_or_create(user=user)
    return profile


@login_required
def dashboard(request):
    profile = get_or_create_profile(request.user)

    projects      = Project.objects.filter(client=profile).order_by("-created_at")
    open_projects = projects.filter(status="open")
    active        = projects.filter(status="in_progress")
    completed     = projects.filter(status="completed")

    total_bids    = Bid.objects.filter(project__client=profile, status="pending").count()
    active_contracts = Contract.objects.filter(
        project__client=profile, status="active"
    ).select_related("project", "bid__developer__user").prefetch_related("milestones")

    pending_milestones = Milestone.objects.filter(
        contract__project__client=profile, status="submitted"
    ).select_related("contract__project")[:5]

    total_spent = Contract.objects.filter(
        project__client=profile, status="completed"
    ).aggregate(total=Sum("total_amount"))["total"] or 0

    recent_projects = projects[:5]

    ctx = {
        "profile":            profile,
        "open_count":         open_projects.count(),
        "active_count":       active.count(),
        "completed_count":    completed.count(),
        "total_bids":         total_bids,
        "active_contracts":   active_contracts,
        "pending_milestones": pending_milestones,
        "total_spent":        total_spent,
        "recent_projects":    recent_projects,
    }
    return render(request, "clients/dashboard.html", ctx)


@login_required
def post_project(request):
    if not request.user.is_client:
        messages.error(request, "Only clients can post projects.")
        return redirect("dashboard")

    profile = get_or_create_profile(request.user)

    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.client = profile
            project.status = "open"
            project.save()
            form.save_m2m()
            messages.success(request, "Project posted successfully! Developers can now bid.")
            return redirect("view_bids", pk=project.pk)
        else:
            for field, errs in form.errors.items():
                for e in errs:
                    messages.error(request, e)
    else:
        form = ProjectForm()

    return render(request, "clients/post_project.html", {"form": form})


@login_required
def my_projects(request):
    profile  = get_or_create_profile(request.user)
    status   = request.GET.get("status", "")
    projects = Project.objects.filter(client=profile).annotate(
        bid_count=Count("bids")
    ).order_by("-created_at")
    if status:
        projects = projects.filter(status=status)
    return render(request, "clients/projects.html", {
        "projects": projects,
        "status":   status,
    })


@login_required
def profile(request):
    return render(request, "clients/profile.html")


@login_required
def project_detail(request, pk):
    client_profile = get_or_create_profile(request.user)
    project = get_object_or_404(Project, pk=pk, client=client_profile)
    return render(request, "clients/project_detail.html", {"project": project})


@login_required
def view_bids(request, pk):
    client_profile = get_or_create_profile(request.user)
    project = get_object_or_404(Project, pk=pk, client=client_profile)
    bids = project.bids.select_related(
        "developer__user"
    ).prefetch_related("developer__skills").order_by("-created_at")
    return render(request, "clients/view_bids.html", {
        "project": project,
        "bids":    bids,
    })


@login_required
def accept_bid(request, pk):
    bid = get_object_or_404(Bid, pk=pk, project__client__user=request.user)
    if request.method == "POST":
        bid.status = "accepted"
        bid.save()
        bid.project.status = "in_progress"
        bid.project.save()
        Bid.objects.filter(project=bid.project).exclude(pk=bid.pk).update(status="rejected")
        Contract.objects.get_or_create(
            project=bid.project,
            defaults={
                "bid": bid,
                "total_amount": bid.amount,
                "start_date": __import__("datetime").date.today(),
            }
        )
        messages.success(request, f"Bid accepted. Contract created with {bid.developer.user.get_full_name() or bid.developer.user.username}.")
        return redirect("client_contracts")
    return render(request, "clients/accept_bid.html", {"bid": bid})


@login_required
def reject_bid(request, pk):
    bid = get_object_or_404(Bid, pk=pk, project__client__user=request.user)
    if request.method == "POST":
        bid.status = "rejected"
        bid.save()
        messages.success(request, "Bid rejected.")
    return redirect("view_bids", pk=bid.project.pk)


@login_required
def my_contracts(request):
    profile = get_or_create_profile(request.user)
    contracts = Contract.objects.filter(
        project__client=profile
    ).select_related("project", "bid__developer__user").prefetch_related("milestones")
    return render(request, "clients/contracts.html", {"contracts": contracts})


@login_required
def contract_detail(request, pk):
    profile  = get_or_create_profile(request.user)
    contract = get_object_or_404(Contract, pk=pk, project__client=profile)
    return render(request, "clients/contract_detail.html", {"contract": contract})


@login_required
def approve_milestone(request, pk):
    from contracts.models import Milestone
    import datetime
    profile   = get_or_create_profile(request.user)
    milestone = get_object_or_404(Milestone, pk=pk, contract__project__client=profile)
    if request.method == "POST":
        milestone.status = "approved"
        milestone.save()
        messages.success(request, f"{milestone.title} approved. You can now release payment.")
        return redirect("client_contract_detail", pk=milestone.contract.pk)
    return render(request, "clients/approve_milestone.html", {"milestone": milestone})


@login_required
def payments(request):
    return render(request, "clients/payments.html")


@login_required
def leave_review(request, contract_pk):
    return render(request, "clients/leave_review.html")
