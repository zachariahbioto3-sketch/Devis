from django.urls import path
from . import views

urlpatterns = [
    path("", views.browse_projects, name="browse_projects"),
    path("<uuid:pk>/", views.project_detail, name="project_detail"),
    path("<uuid:pk>/bid/", views.place_bid, name="place_bid"),
    path("search/", views.search_projects, name="search_projects"),
]
