from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def browse_projects(request):
    return render(request, "projects/browse.html")

def project_detail(request, pk):
    return render(request, "projects/detail.html")

@login_required
def place_bid(request, pk):
    return render(request, "projects/place_bid.html")

def search_projects(request):
    return render(request, "projects/browse.html")
