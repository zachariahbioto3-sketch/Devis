from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    return render(request, "clients/dashboard.html")

@login_required
def profile(request):
    return render(request, "clients/profile.html")

@login_required
def my_projects(request):
    return render(request, "clients/projects.html")

@login_required
def post_project(request):
    return render(request, "clients/post_project.html")

@login_required
def project_detail(request, pk):
    return render(request, "clients/project_detail.html")

@login_required
def view_bids(request, pk):
    return render(request, "clients/view_bids.html")

@login_required
def accept_bid(request, pk):
    return render(request, "clients/accept_bid.html")

@login_required
def reject_bid(request, pk):
    return render(request, "clients/reject_bid.html")

@login_required
def my_contracts(request):
    return render(request, "clients/contracts.html")

@login_required
def contract_detail(request, pk):
    return render(request, "clients/contract_detail.html")

@login_required
def approve_milestone(request, pk):
    return render(request, "clients/approve_milestone.html")

@login_required
def payments(request):
    return render(request, "clients/payments.html")

@login_required
def leave_review(request, contract_pk):
    return render(request, "clients/leave_review.html")
