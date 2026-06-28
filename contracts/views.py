from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def contract_detail(request, pk):
    return render(request, "contracts/detail.html")

@login_required
def add_milestone(request, pk):
    return render(request, "contracts/add_milestone.html")

@login_required
def milestone_detail(request, pk):
    return render(request, "contracts/milestone_detail.html")
