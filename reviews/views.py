from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def review_developer(request, dev_pk):
    return render(request, "reviews/review.html")

@login_required
def review_product(request, product_pk):
    return render(request, "reviews/review.html")
