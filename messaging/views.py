from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def inbox(request):
    return render(request, "messaging/inbox.html")

@login_required
def thread_detail(request, thread_pk):
    return render(request, "messaging/thread.html")

@login_required
def new_thread(request, user_pk):
    return render(request, "messaging/new_thread.html")
