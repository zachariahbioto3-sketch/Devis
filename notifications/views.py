from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def notifications(request):
    return render(request, "notifications/list.html")

@login_required
def mark_read(request, pk):
    return render(request, "notifications/list.html")

@login_required
def mark_all_read(request):
    return render(request, "notifications/list.html")
