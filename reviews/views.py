from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Review
from django.contrib.auth import get_user_model

User = get_user_model()


@login_required
def review_developer(request, dev_pk):
    from developers.models import DeveloperProfile
    from contracts.models import Contract
    dev_profile = get_object_or_404(DeveloperProfile, pk=dev_pk)

    already = Review.objects.filter(
        reviewer=request.user, reviewee=dev_profile.user
    ).exists()
    if already:
        messages.info(request, "You have already reviewed this developer.")
        return redirect("dev_public_profile", slug=dev_profile.slug)

    if request.method == "POST":
        rating  = request.POST.get("rating")
        comment = request.POST.get("comment", "").strip()
        if not rating or not comment:
            messages.error(request, "Rating and comment are required.")
        else:
            Review.objects.create(
                reviewer=request.user,
                reviewee=dev_profile.user,
                review_for="developer",
                rating=int(rating),
                comment=comment,
            )
            return redirect("dev_public_profile", slug=dev_profile.slug)

    return render(request, "reviews/review.html", {"reviewee": dev_profile.user, "type": "developer"})


@login_required
def review_product(request, product_pk):
    from store.models import SoftwareProduct, ProductPurchase
    product = get_object_or_404(SoftwareProduct, pk=product_pk)

    purchased = ProductPurchase.objects.filter(product=product, buyer=request.user).exists()
    if not purchased:
        messages.error(request, "You can only review products you have purchased.")
        return redirect("product_detail", slug=product.slug)

    already = Review.objects.filter(
        reviewer=request.user, product=product
    ).exists()
    if already:
        messages.info(request, "You have already reviewed this product.")
        return redirect("product_detail", slug=product.slug)

    if request.method == "POST":
        rating  = request.POST.get("rating")
        comment = request.POST.get("comment", "").strip()
        if not rating or not comment:
            messages.error(request, "Rating and comment are required.")
        else:
            Review.objects.create(
                reviewer=request.user,
                product=product,
                review_for="product",
                rating=int(rating),
                comment=comment,
            )
            return redirect("product_detail", slug=product.slug)

    return render(request, "reviews/review.html", {"reviewee": product, "type": "product"})
