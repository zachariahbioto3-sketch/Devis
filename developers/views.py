from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from developers.models import DeveloperProfile, DeveloperSkill, Skill, Certification, PortfolioProject
from developers.forms import DeveloperProfileForm, PortfolioProjectForm, CertificationForm
from projects.models import Bid
from contracts.models import Contract, Milestone, Deliverable


def get_or_create_profile(user):
    profile, _ = DeveloperProfile.objects.get_or_create(
        user=user,
        defaults={"slug": user.username}
    )
    return profile


@login_required
def dashboard(request):
    profile = get_or_create_profile(request.user)

    all_bids      = Bid.objects.filter(developer=profile).select_related("project")
    pending_bids  = all_bids.filter(status="pending")
    accepted_bids = all_bids.filter(status="accepted")

    active_contracts = Contract.objects.filter(
        bid__developer=profile, status="active"
    ).select_related("project", "bid").prefetch_related("milestones")

    completed_contracts = Contract.objects.filter(
        bid__developer=profile, status="completed"
    )

    pending_milestones = Milestone.objects.filter(
        contract__bid__developer=profile,
        status="in_progress"
    ).select_related("contract__project")[:5]

    total_earned = Milestone.objects.filter(
        contract__bid__developer=profile,
        status="paid"
    ).aggregate(total=Sum("amount"))["total"] or 0

    skills = DeveloperSkill.objects.filter(
        developer=profile
    ).select_related("skill")[:8]

    try:
        subscription = profile.subscription
    except Exception:
        subscription = None

    ctx = {
        "profile":            profile,
        "pending_bids":       pending_bids,
        "pending_bids_count": pending_bids.count(),
        "active_contracts":   active_contracts,
        "active_count":       active_contracts.count(),
        "completed_count":    completed_contracts.count(),
        "pending_milestones": pending_milestones,
        "total_earned":       total_earned,
        "skills":             skills,
        "subscription":       subscription,
        "total_bids":         all_bids.count(),
    }
    return render(request, "developers/dashboard.html", ctx)


@login_required
def my_contracts(request):
    profile = get_or_create_profile(request.user)
    contracts = Contract.objects.filter(
        bid__developer=profile
    ).select_related("project", "bid").prefetch_related("milestones").order_by("-created_at")
    return render(request, "developers/contracts.html", {"contracts": contracts})


@login_required
def contract_detail(request, pk):
    profile  = get_or_create_profile(request.user)
    contract = get_object_or_404(Contract, pk=pk, bid__developer=profile)
    milestones = contract.milestones.all().prefetch_related("deliverables")
    return render(request, "developers/contract_detail.html", {
        "contract":   contract,
        "milestones": milestones,
    })


@login_required
def submit_deliverable(request, pk):
    profile   = get_or_create_profile(request.user)
    milestone = get_object_or_404(
        Milestone, pk=pk, contract__bid__developer=profile
    )

    if milestone.status not in ["pending", "in_progress"]:
        messages.error(request, "This milestone cannot be submitted right now.")
        return redirect("dev_contract_detail", pk=milestone.contract.pk)

    if request.method == "POST":
        description = request.POST.get("description", "").strip()
        file_url    = request.POST.get("file_url", "").strip()
        file        = request.FILES.get("file")

        if not description:
            messages.error(request, "Please describe what you have delivered.")
        else:
            Deliverable.objects.create(
                milestone=milestone,
                description=description,
                file_url=file_url,
                file=file if file else None,
            )
            milestone.status = "submitted"
            milestone.save()
            messages.success(request, f'"{milestone.title}" submitted for client review.')
            return redirect("dev_contract_detail", pk=milestone.contract.pk)

    return render(request, "developers/submit_deliverable.html", {
        "milestone": milestone,
    })


@login_required
def my_bids(request):
    profile = get_or_create_profile(request.user)
    bids = Bid.objects.filter(developer=profile).select_related("project").order_by("-created_at")
    return render(request, "developers/bids.html", {"bids": bids})


@login_required
def withdraw_bid(request, pk):
    profile = get_or_create_profile(request.user)
    bid = get_object_or_404(Bid, pk=pk, developer=profile, status="pending")
    if request.method == "POST":
        bid.status = "withdrawn"
        bid.save()
        messages.success(request, "Bid withdrawn.")
    return redirect("dev_bids")


@login_required
def earnings(request):
    profile = get_or_create_profile(request.user)
    paid_milestones = Milestone.objects.filter(
        contract__bid__developer=profile, status="paid"
    ).select_related("contract__project").order_by("-contract__created_at")
    total = paid_milestones.aggregate(total=Sum("amount"))["total"] or 0
    return render(request, "developers/earnings.html", {
        "paid_milestones": paid_milestones,
        "total":           total,
    })


@login_required
def profile(request):
    dev_profile = get_or_create_profile(request.user)

    if request.method == "POST":
        form = DeveloperProfileForm(request.POST, request.FILES, instance=dev_profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect("dev_profile")
        else:
            for field, errs in form.errors.items():
                for e in errs:
                    messages.error(request, e)
    else:
        form = DeveloperProfileForm(instance=dev_profile)

    return render(request, "developers/profile.html", {
        "dev_profile": dev_profile,
        "form": form,
    })


@login_required
def portfolio(request):
    dev_profile = get_or_create_profile(request.user)
    projects = dev_profile.portfolio_projects.all()
    return render(request, "developers/portfolio.html", {
        "dev_profile": dev_profile,
        "projects":    projects,
    })


@login_required
def add_portfolio_project(request):
    dev_profile = get_or_create_profile(request.user)

    if request.method == "POST":
        form = PortfolioProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.developer = dev_profile
            project.save()
            messages.success(request, "Portfolio project added.")
            return redirect("dev_portfolio")
        else:
            for field, errs in form.errors.items():
                for e in errs:
                    messages.error(request, e)
    else:
        form = PortfolioProjectForm()

    return render(request, "developers/add_portfolio.html", {"form": form})


@login_required
def delete_portfolio_project(request, pk):
    dev_profile = get_or_create_profile(request.user)
    project = get_object_or_404(PortfolioProject, pk=pk, developer=dev_profile)
    if request.method == "POST":
        project.delete()
        messages.success(request, "Project removed.")
    return redirect("dev_portfolio")


@login_required
def manage_skills(request):
    dev_profile = get_or_create_profile(request.user)
    all_skills  = Skill.objects.all().order_by("name")
    dev_skills  = DeveloperSkill.objects.filter(developer=dev_profile).select_related("skill")

    # skills already added by this developer
    added_skill_ids = dev_skills.values_list("skill_id", flat=True)
    available_skills = all_skills.exclude(pk__in=added_skill_ids)

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "add":
            skill_id = request.POST.get("skill_id")
            level    = request.POST.get("level", "intermediate")
            skill    = get_object_or_404(Skill, pk=skill_id)
            DeveloperSkill.objects.get_or_create(
                developer=dev_profile, skill=skill,
                defaults={"level": level}
            )
            messages.success(request, f"{skill.name} added.")
        elif action == "remove":
            ds_id = request.POST.get("ds_id")
            DeveloperSkill.objects.filter(pk=ds_id, developer=dev_profile).delete()
            messages.success(request, "Skill removed.")
        return redirect("dev_skills")

    return render(request, "developers/skills.html", {
        "dev_profile":     dev_profile,
        "all_skills":      all_skills,
        "available_skills": available_skills,
        "dev_skills":      dev_skills,
    })


@login_required
def manage_certifications(request):
    dev_profile = get_or_create_profile(request.user)
    certs = dev_profile.certifications.all().order_by("-issued_date")

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "add":
            form = CertificationForm(request.POST)
            if form.is_valid():
                cert = form.save(commit=False)
                cert.developer = dev_profile
                cert.save()
                messages.success(request, "Certification added.")
                return redirect("dev_certifications")
            else:
                for field, errs in form.errors.items():
                    for e in errs:
                        messages.error(request, e)
        elif action == "delete":
            cert_pk = request.POST.get("cert_pk")
            Certification.objects.filter(pk=cert_pk, developer=dev_profile).delete()
            messages.success(request, "Certification removed.")
            return redirect("dev_certifications")
        form_obj = CertificationForm(request.POST)
    else:
        form_obj = CertificationForm()

    return render(request, "developers/certifications.html", {
        "dev_profile": dev_profile,
        "certs":       certs,
        "form":        form_obj,
    })


@login_required
def metrics(request):
    profile = get_or_create_profile(request.user)

    all_bids = Bid.objects.filter(developer=profile)
    total_bids   = all_bids.count()
    accepted     = all_bids.filter(status="accepted").count()
    win_rate     = round((accepted / total_bids * 100) if total_bids else 0, 1)

    total_earned = Milestone.objects.filter(
        contract__bid__developer=profile, status="paid"
    ).aggregate(total=Sum("amount"))["total"] or 0

    completed_contracts = Contract.objects.filter(
        bid__developer=profile, status="completed"
    ).count()

    return render(request, "developers/metrics.html", {
        "profile":             profile,
        "total_bids":          total_bids,
        "accepted_bids":       accepted,
        "win_rate":            win_rate,
        "total_earned":        total_earned,
        "completed_contracts": completed_contracts,
    })


@login_required
def subscription(request):
    from developers.models import Subscription
    import os
    dev_profile = get_or_create_profile(request.user)

    try:
        sub = dev_profile.subscription
    except Exception:
        sub = None

    if request.method == "POST":
        phone = request.POST.get("phone", "").strip() or request.user.phone
        plan  = request.POST.get("plan", "pro")

        if not phone:
            messages.error(request, "Please enter your M-Pesa phone number.")
            return render(request, "developers/subscription.html", {"subscription": sub})

        from payments.mpesa import stk_push
        amount = 999

        codespace_name = os.environ.get("CODESPACE_NAME", "")
        callback_url = (
            f"https://{codespace_name}-8000.app.github.dev/payments/mpesa/callback/"
            if codespace_name
            else request.build_absolute_uri("/payments/mpesa/callback/")
        )

        try:
            result = stk_push(
                phone=phone,
                amount=amount,
                reference="DEVIS-SUB",
                description="Pro subscription",
                callback_url=callback_url,
            )
            if result.get("ResponseCode") == "0":
                import datetime
                if sub:
                    sub.plan   = "pro"
                    sub.status = "active"
                    sub.end_date = datetime.date.today() + datetime.timedelta(days=30)
                    sub.amount_paid = amount
                    sub.save()
                else:
                    Subscription.objects.create(
                        developer=dev_profile,
                        plan="pro",
                        status="active",
                        end_date=datetime.date.today() + datetime.timedelta(days=30),
                        amount_paid=amount,
                    )
                messages.success(request, "M-Pesa prompt sent. Enter your PIN to activate Pro plan.")
                return redirect("dev_subscription")
            else:
                messages.error(request, f"M-Pesa error: {result.get('errorMessage', 'Unknown error')}")
        except Exception as e:
            messages.error(request, f"Could not reach M-Pesa. ({e})")

    return render(request, "developers/subscription.html", {
        "subscription": sub,
        "phone": request.user.phone,
    })


@login_required
def my_products(request):
    dev_profile = get_or_create_profile(request.user)
    from store.models import SoftwareProduct
    products = SoftwareProduct.objects.filter(developer=dev_profile)
    return render(request, "developers/products.html", {"products": products})


@login_required
def upload_product(request):
    from store.forms import SoftwareProductForm
    from django.utils.text import slugify
    from store.models import SoftwareProduct

    dev_profile = get_or_create_profile(request.user)

    if request.method == "POST":
        form = SoftwareProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.developer = dev_profile
            base_slug = slugify(product.title)
            slug = base_slug
            counter = 1
            while SoftwareProduct.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            product.slug = slug
            product.save()
            messages.success(request, "Product listed on the marketplace.")
            return redirect("dev_products")
        else:
            for field, errs in form.errors.items():
                for e in errs:
                    messages.error(request, e)
    else:
        form = SoftwareProductForm()

    return render(request, "developers/upload_product.html", {"form": form})


@login_required
def edit_product(request, pk):
    from store.forms import SoftwareProductForm
    from store.models import SoftwareProduct
    dev_profile = get_or_create_profile(request.user)
    product = get_object_or_404(SoftwareProduct, pk=pk, developer=dev_profile)

    if request.method == "POST":
        form = SoftwareProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated.")
            return redirect("dev_products")
    else:
        form = SoftwareProductForm(instance=product)

    return render(request, "developers/edit_product.html", {"form": form, "product": product})


@login_required
def delete_product(request, pk):
    from store.models import SoftwareProduct
    dev_profile = get_or_create_profile(request.user)
    product = get_object_or_404(SoftwareProduct, pk=pk, developer=dev_profile)
    if request.method == "POST":
        product.delete()
        messages.success(request, "Product removed from marketplace.")
    return redirect("dev_products")


def public_profile(request, slug):
    dev_profile = get_object_or_404(DeveloperProfile, slug=slug)
    return render(request, "developers/public_profile.html", {"dev_profile": dev_profile})
