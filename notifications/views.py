from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Notification


@login_required
def notifications(request):
    notifs = Notification.objects.filter(user=request.user).order_by("-created_at")
    unread = notifs.filter(is_read=False).count()
    return render(request, "notifications/list.html", {
        "notifications": notifs,
        "unread": unread,
    })


@login_required
def mark_read(request, pk):
    notif = get_object_or_404(Notification, pk=pk, user=request.user)
    notif.is_read = True
    notif.save()
    if notif.link:
        return redirect(notif.link)
    return redirect("notifications")


@login_required
def mark_all_read(request):
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    return redirect("notifications")
