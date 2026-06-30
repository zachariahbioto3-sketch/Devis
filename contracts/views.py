from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Contract, Milestone, Deliverable


@login_required
def contract_detail(request, pk):
    contract = get_object_or_404(Contract, pk=pk)
    return render(request, "contracts/detail.html", {"contract": contract})


@login_required
def add_milestone(request, pk):
    contract = get_object_or_404(Contract, pk=pk)

    # only the developer on this contract can add milestones
    if not hasattr(request.user, "dev_profile"):
        messages.error(request, "Only developers can add milestones.")
        return redirect("dev_contracts")

    if request.method == "POST":
        title       = request.POST.get("title", "").strip()
        description = request.POST.get("description", "").strip()
        amount      = request.POST.get("amount")
        due_date    = request.POST.get("due_date") or None

        if not title or not amount:
            messages.error(request, "Title and amount are required.")
        else:
            order = contract.milestones.count() + 1
            Milestone.objects.create(
                contract=contract,
                title=title,
                description=description,
                amount=amount,
                due_date=due_date,
                order=order,
                status="pending",
            )
            messages.success(request, f"Milestone '{title}' added.")
            return redirect("dev_contract_detail", pk=pk)

    return render(request, "contracts/add_milestone.html", {"contract": contract})


@login_required
def milestone_detail(request, pk):
    milestone = get_object_or_404(Milestone, pk=pk)
    return render(request, "contracts/milestone_detail.html", {"milestone": milestone})


@login_required
def start_milestone(request, pk):
    milestone = get_object_or_404(Milestone, pk=pk)
    if request.method == "POST":
        milestone.status = "in_progress"
        milestone.save()
        messages.success(request, f"'{milestone.title}' marked as in progress.")
    return redirect("dev_contract_detail", pk=milestone.contract.pk)
