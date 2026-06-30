from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.utils.text import slugify
from .models import SoftwareProduct, ProductPurchase
from .forms import SoftwareProductForm


def marketplace(request):
    products = SoftwareProduct.objects.filter(is_active=True).select_related(
        "developer__user"
    ).order_by("-created_at")

    category = request.GET.get("category", "")
    search   = request.GET.get("q", "")

    if category:
        products = products.filter(category=category)
    if search:
        products = products.filter(
            Q(title__icontains=search) |
            Q(short_description__icontains=search) |
            Q(tech_stack__icontains=search)
        )

    categories = SoftwareProduct.CATEGORY_CHOICES
    total = products.count()

    return render(request, "store/marketplace.html", {
        "products":   products,
        "categories": categories,
        "category":   category,
        "search":     search,
        "total":      total,
    })


def product_detail(request, slug):
    product = get_object_or_404(
        SoftwareProduct.objects.select_related("developer__user"),
        slug=slug, is_active=True
    )

    already_bought = False
    purchase = None
    if request.user.is_authenticated:
        purchase = ProductPurchase.objects.filter(
            product=product, buyer=request.user
        ).first()
        already_bought = purchase is not None

    related = SoftwareProduct.objects.filter(
        category=product.category, is_active=True
    ).exclude(pk=product.pk)[:3]

    return render(request, "store/product_detail.html", {
        "product":        product,
        "already_bought": already_bought,
        "purchase":       purchase,
        "related":        related,
    })


@login_required
def purchase_product(request, slug):
    product = get_object_or_404(SoftwareProduct, slug=slug, is_active=True)

    existing = ProductPurchase.objects.filter(product=product, buyer=request.user).first()
    if existing:
        messages.info(request, "You already own this product.")
        return redirect("product_detail", slug=slug)

    if request.method == "POST":
        phone = request.POST.get("phone", "").strip() or request.user.phone

        if not phone:
            messages.error(request, "Please enter your M-Pesa phone number.")
            return render(request, "store/purchase.html", {"product": product})

        from payments.mpesa import stk_push
        from payments.models import Payment
        import os

        purchase = ProductPurchase.objects.create(
            product=product,
            buyer=request.user,
            amount_paid=product.price,
        )

        payment = Payment.objects.create(
            payment_type="product",
            product_purchase=purchase,
            amount=product.price,
            method="mpesa",
            status="pending",
            platform_fee=product.price * 15 / 100,  # 15% on product sales
        )

        codespace_name = os.environ.get("CODESPACE_NAME", "")
        if codespace_name:
            callback_url = f"https://{codespace_name}-8000.app.github.dev/payments/mpesa/callback/"
        else:
            callback_url = request.build_absolute_uri("/payments/mpesa/callback/")

        try:
            result = stk_push(
                phone=phone,
                amount=product.price,
                reference=str(purchase.pk)[:12],
                description="Product purchase",
                callback_url=callback_url,
            )
            if result.get("ResponseCode") == "0":
                payment.mpesa_ref = result.get("CheckoutRequestID", "")
                payment.save()
                messages.success(request, f"M-Pesa prompt sent to {phone}. Enter your PIN to complete the purchase.")
                return redirect("product_detail", slug=slug)
            else:
                payment.status = "failed"
                payment.save()
                purchase.delete()
                messages.error(request, f"M-Pesa error: {result.get('errorMessage', 'Unknown error')}")
        except Exception as e:
            payment.status = "failed"
            payment.save()
            purchase.delete()
            messages.error(request, f"Could not reach M-Pesa. Please try again. ({e})")

    return render(request, "store/purchase.html", {
        "product": product,
        "phone":   request.user.phone,
    })


@login_required
def download_product(request, slug, token):
    product = get_object_or_404(SoftwareProduct, slug=slug)
    purchase = get_object_or_404(
        ProductPurchase, product=product, buyer=request.user, download_token=token
    )
    return render(request, "store/download.html", {
        "product":  product,
        "purchase": purchase,
    })
