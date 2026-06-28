from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Q
from developers.models import DeveloperProfile, DeveloperSkill
from projects.models import Bid
from contracts.models import Contract, Milestone


def get_or_create_profile(user):
    profile, _ = DeveloperProfile.objects.get_or_create(
        user=user,
        defaults={'slug': user.username}
    )
    return profile


@login_required
def dashboard(request):
    profile = get_or_create_profile(request.user)

    # Bids
    all_bids      = Bid.objects.filter(developer=profile).select_related('project')
    pending_bids  = all_bids.filter(status='pending')
    accepted_bids = all_bids.filter(status='accepted')

    # Contracts
    active_contracts = Contract.objects.filter(
        bid__developer=profile, status='active'
    ).select_related('project', 'bid')

    completed_contracts = Contract.objects.filter(
        bid__developer=profile, status='completed'
    )

    # Milestones pending submission
    pending_milestones = Milestone.objects.filter(
        contract__bid__developer=profile,
        status='in_progress'
    ).select_related('contract__project')[:5]

    # Earnings
    total_earned = Milestone.objects.filter(
        contract__bid__developer=profile,
        status='paid'
    ).aggregate(total=Sum('amount'))['total'] or 0

    # Skills
    skills = DeveloperSkill.objects.filter(
        developer=profile
    ).select_related('skill')[:8]

    # Subscription
    try:
        subscription = profile.subscription
    except Exception:
        subscription = None

    ctx = {
        'profile':              profile,
        'pending_bids':         pending_bids,
        'pending_bids_count':   pending_bids.count(),
        'active_contracts':     active_contracts,
        'active_count':         active_contracts.count(),
        'completed_count':      completed_contracts.count(),
        'pending_milestones':   pending_milestones,
        'total_earned':         total_earned,
        'skills':               skills,
        'subscription':         subscription,
        'total_bids':           all_bids.count(),
    }
    return render(request, 'developers/dashboard.html', ctx)


@login_required
def profile(request):
    return render(request, 'developers/profile.html')

@login_required
def portfolio(request):
    return render(request, 'developers/portfolio.html')

@login_required
def add_portfolio_project(request):
    return render(request, 'developers/add_portfolio.html')

@login_required
def delete_portfolio_project(request, pk):
    return render(request, 'developers/portfolio.html')

@login_required
def manage_skills(request):
    return render(request, 'developers/skills.html')

@login_required
def manage_certifications(request):
    return render(request, 'developers/certifications.html')

@login_required
def my_bids(request):
    return render(request, 'developers/bids.html')

@login_required
def withdraw_bid(request, pk):
    return render(request, 'developers/bids.html')

@login_required
def my_contracts(request):
    return render(request, 'developers/contracts.html')

@login_required
def contract_detail(request, pk):
    return render(request, 'developers/contract_detail.html')

@login_required
def submit_deliverable(request, pk):
    return render(request, 'developers/submit_deliverable.html')

@login_required
def earnings(request):
    return render(request, 'developers/earnings.html')

@login_required
def metrics(request):
    return render(request, 'developers/metrics.html')

@login_required
def subscription(request):
    return render(request, 'developers/subscription.html')

@login_required
def my_products(request):
    return render(request, 'developers/products.html')

@login_required
def upload_product(request):
    return render(request, 'developers/upload_product.html')

@login_required
def edit_product(request, pk):
    return render(request, 'developers/edit_product.html')

@login_required
def delete_product(request, pk):
    return render(request, 'developers/products.html')

def public_profile(request, slug):
    return render(request, 'developers/public_profile.html')
