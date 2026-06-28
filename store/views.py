from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def marketplace(request):
    return render(request, "store/marketplace.html")

def product_detail(request, slug):
    return render(request, "store/product_detail.html")

@login_required
def purchase_product(request, slug):
    return render(request, "store/purchase.html")

@login_required
def download_product(request, slug, token):
    return render(request, "store/download.html")
