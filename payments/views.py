from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

@login_required
def pay_milestone(request, milestone_pk):
    return render(request, "payments/pay.html")

@login_required
def pay_subscription(request):
    return render(request, "payments/subscription.html")

def mpesa_initiate(request):
    return render(request, "payments/pay.html")

@csrf_exempt
def mpesa_callback(request):
    return render(request, "payments/pay.html")
