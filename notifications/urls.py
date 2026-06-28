from django.urls import path
from . import views

urlpatterns = [
    path("", views.notifications, name="notifications"),
    path("<uuid:pk>/read/", views.mark_read, name="mark_notification_read"),
    path("read-all/", views.mark_all_read, name="mark_all_read"),
]
