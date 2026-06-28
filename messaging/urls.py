from django.urls import path
from . import views

urlpatterns = [
    path("", views.inbox, name="inbox"),
    path("<uuid:thread_pk>/", views.thread_detail, name="thread_detail"),
    path("new/<uuid:user_pk>/", views.new_thread, name="new_thread"),
]
