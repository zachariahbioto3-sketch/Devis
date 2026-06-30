from django.urls import path
from . import views

urlpatterns = [
    path("<uuid:pk>/",                  views.contract_detail,  name="contract_detail"),
    path("<uuid:pk>/milestones/add/",   views.add_milestone,    name="add_milestone"),
    path("milestones/<uuid:pk>/",       views.milestone_detail, name="milestone_detail"),
    path("milestones/<uuid:pk>/start/", views.start_milestone,  name="start_milestone"),
]
