from django.urls import path
from . import views

urlpatterns = [
    path("", views.marketplace, name="marketplace"),
    path("<slug:slug>/", views.product_detail, name="product_detail"),
    path("<slug:slug>/buy/", views.purchase_product, name="purchase_product"),
    path("<slug:slug>/download/<uuid:token>/", views.download_product, name="download_product"),
]
