from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages as django_messages
from django.db.models import Max
from .models import Thread, Message

User = get_user_model()


@login_required
def inbox(request):
    threads = Thread.objects.filter(
        participants=request.user
    ).prefetch_related("participants", "messages").annotate(
        last_activity=Max("messages__created_at")
    ).order_by("-last_activity")

    return render(request, "messaging/inbox.html", {"threads": threads})


@login_required
def thread_detail(request, thread_pk):
    thread = get_object_or_404(Thread, pk=thread_pk, participants=request.user)
    other_user = thread.participants.exclude(pk=request.user.pk).first()

    if request.method == "POST":
        body = request.POST.get("body", "").strip()
        if body:
            Message.objects.create(thread=thread, sender=request.user, body=body)
            return redirect("thread_detail", thread_pk=thread.pk)

    # mark unread messages as read
    thread.messages.exclude(sender=request.user).update(is_read=True)

    msgs = thread.messages.select_related("sender").order_by("created_at")

    return render(request, "messaging/thread.html", {
        "thread":     thread,
        "other_user": other_user,
        "messages_list": msgs,
    })


@login_required
def new_thread(request, user_pk):
    other_user = get_object_or_404(User, pk=user_pk)

    if other_user == request.user:
        django_messages.error(request, "You cannot message yourself.")
        return redirect("inbox")

    existing = Thread.objects.filter(participants=request.user).filter(
        participants=other_user
    ).first()

    if existing:
        return redirect("thread_detail", thread_pk=existing.pk)

    thread = Thread.objects.create()
    thread.participants.add(request.user, other_user)

    if request.method == "POST":
        body = request.POST.get("body", "").strip()
        if body:
            Message.objects.create(thread=thread, sender=request.user, body=body)

    return redirect("thread_detail", thread_pk=thread.pk)
