from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="client_dashboard"),
    path("profile/", views.profile, name="client_profile"),
    path("projects/", views.my_projects, name="client_projects"),
    path("projects/new/", views.post_project, name="post_project"),
    path("projects/<uuid:pk>/", views.project_detail, name="client_project_detail"),
    path("projects/<uuid:pk>/bids/", views.view_bids, name="view_bids"),
    path("bids/<uuid:pk>/accept/", views.accept_bid, name="accept_bid"),
    path("bids/<uuid:pk>/reject/", views.reject_bid, name="reject_bid"),
    path("contracts/", views.my_contracts, name="client_contracts"),
    path("contracts/<uuid:pk>/", views.contract_detail, name="client_contract_detail"),
    path("milestones/<uuid:pk>/approve/", views.approve_milestone, name="approve_milestone"),
    path("payments/", views.payments, name="client_payments"),
    path("reviews/new/<uuid:contract_pk>/", views.leave_review, name="client_leave_review"),
]
