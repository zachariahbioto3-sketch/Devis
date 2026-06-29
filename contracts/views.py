from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Contract, Milestone, Deliverable


@login_required
def contract_detail(request, pk):
    user = request.user
    if user.is_client:
        contract = get_object_or_404(Contract, pk=pk, project__client__user=user)
        return render(request, "clients/contract_detail.html", {"contract": contract})
    elif user.is_developer:
        contract = get_object_or_404(Contract, pk=pk, bid__developer__user=user)
        return render(request, "developers/contract_detail.html", {"contract": contract})
    return redirect("home")


@login_required
def add_milestone(request, pk):
    contract = get_object_or_404(Contract, pk=pk, project__client__user=request.user)
    if request.method == "POST":
        title      = request.POST.get("title", "").strip()
        description = request.POST.get("description", "").strip()
        amount     = request.POST.get("amount")
        due_date   = request.POST.get("due_date") or None
        order      = contract.milestones.count() + 1
        if title and amount:
            Milestone.objects.create(
                contract=contract,
                title=title,
                description=description,
                amount=amount,
                due_date=due_date,
                order=order,
            )
            messages.success(request, f"Milestone '{title}' added.")
            return redirect("client_contract_detail", pk=contract.pk)
        else:
            messages.error(request, "Title and amount are required.")
    return render(request, "contracts/add_milestone.html", {"contract": contract})


@login_required
def milestone_detail(request, pk):
    user = request.user
    if user.is_developer:
        milestone = get_object_or_404(Milestone, pk=pk, contract__bid__developer__user=user)
    else:
        milestone = get_object_or_404(Milestone, pk=pk, contract__project__client__user=user)
    return render(request, "contracts/milestone_detail.html", {"milestone": milestone})
