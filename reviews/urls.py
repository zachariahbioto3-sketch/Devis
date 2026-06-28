from django.urls import path
from . import views

urlpatterns = [
    path("dev/<uuid:dev_pk>/", views.review_developer, name="review_developer"),
    path("product/<uuid:product_pk>/", views.review_product, name="review_product"),
]
