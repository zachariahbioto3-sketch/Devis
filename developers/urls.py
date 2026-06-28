from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dev_dashboard"),
    path("profile/", views.profile, name="dev_profile"),
    path("portfolio/", views.portfolio, name="dev_portfolio"),
    path("portfolio/add/", views.add_portfolio_project, name="add_portfolio_project"),
    path("portfolio/<uuid:pk>/delete/", views.delete_portfolio_project, name="delete_portfolio_project"),
    path("skills/", views.manage_skills, name="dev_skills"),
    path("certifications/", views.manage_certifications, name="dev_certifications"),
    path("bids/", views.my_bids, name="dev_bids"),
    path("bids/<uuid:pk>/withdraw/", views.withdraw_bid, name="withdraw_bid"),
    path("contracts/", views.my_contracts, name="dev_contracts"),
    path("contracts/<uuid:pk>/", views.contract_detail, name="dev_contract_detail"),
    path("milestones/<uuid:pk>/submit/", views.submit_deliverable, name="submit_deliverable"),
    path("earnings/", views.earnings, name="dev_earnings"),
    path("metrics/", views.metrics, name="dev_metrics"),
    path("subscription/", views.subscription, name="dev_subscription"),
    path("products/", views.my_products, name="dev_products"),
    path("products/new/", views.upload_product, name="upload_product"),
    path("products/<uuid:pk>/edit/", views.edit_product, name="edit_product"),
    path("products/<uuid:pk>/delete/", views.delete_product, name="delete_product"),
    path("<slug:slug>/", views.public_profile, name="dev_public_profile"),
]
