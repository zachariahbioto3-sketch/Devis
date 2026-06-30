from django.urls import path
from . import views

urlpatterns = [
    path("", views.browse_developers, name="browse_developers"),
]
