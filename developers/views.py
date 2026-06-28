from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    return render(request, "developers/dashboard.html")

@login_required
def profile(request):
    return render(request, "developers/profile.html")

@login_required
def portfolio(request):
    return render(request, "developers/portfolio.html")

@login_required
def add_portfolio_project(request):
    return render(request, "developers/add_portfolio.html")

@login_required
def delete_portfolio_project(request, pk):
    return render(request, "developers/portfolio.html")

@login_required
def manage_skills(request):
    return render(request, "developers/skills.html")

@login_required
def manage_certifications(request):
    return render(request, "developers/certifications.html")

@login_required
def my_bids(request):
    return render(request, "developers/bids.html")

@login_required
def withdraw_bid(request, pk):
    return render(request, "developers/bids.html")

@login_required
def my_contracts(request):
    return render(request, "developers/contracts.html")

@login_required
def contract_detail(request, pk):
    return render(request, "developers/contract_detail.html")

@login_required
def submit_deliverable(request, pk):
    return render(request, "developers/submit_deliverable.html")

@login_required
def earnings(request):
    return render(request, "developers/earnings.html")

@login_required
def metrics(request):
    return render(request, "developers/metrics.html")

@login_required
def subscription(request):
    return render(request, "developers/subscription.html")

@login_required
def my_products(request):
    return render(request, "developers/products.html")

@login_required
def upload_product(request):
    return render(request, "developers/upload_product.html")

@login_required
def edit_product(request, pk):
    return render(request, "developers/edit_product.html")

@login_required
def delete_product(request, pk):
    return render(request, "developers/products.html")

def public_profile(request, slug):
    return render(request, "developers/public_profile.html")
