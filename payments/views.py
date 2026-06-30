import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib import messages
from django.conf import settings
from contracts.models import Milestone
from payments.models import Payment
from .mpesa import stk_push


@login_required
def pay_milestone(request, milestone_pk):
    milestone = get_object_or_404(
        Milestone, pk=milestone_pk,
        contract__project__client__user=request.user,
        status="approved"
    )

    if request.method == "POST":
        phone = request.POST.get("phone", "").strip()
        if not phone:
            phone = request.user.phone

        if not phone:
            messages.error(request, "Please enter your M-Pesa phone number.")
            return render(request, "payments/pay.html", {"milestone": milestone})

        # Reuse existing payment record if one exists (e.g. from a failed attempt)
        payment, created = Payment.objects.get_or_create(
            milestone=milestone,
            defaults={
                "payment_type": "milestone",
                "amount": milestone.amount,
                "method": "mpesa",
                "status": "pending",
                "platform_fee": milestone.amount * 10 / 100,
            }
        )
        if not created:
            if payment.status == "completed":
                messages.info(request, "This milestone has already been paid.")
                return redirect("client_contract_detail", pk=milestone.contract.pk)
            payment.status = "pending"
            payment.save()

        # Daraja requires a real public HTTPS URL — use the Codespace public URL
        import os
        codespace_name = os.environ.get("CODESPACE_NAME", "")
        if codespace_name:
            callback_url = f"https://{codespace_name}-8000.app.github.dev/payments/mpesa/callback/"
        else:
            callback_url = request.build_absolute_uri("/payments/mpesa/callback/")

        try:
            result = stk_push(
                phone=phone,
                amount=milestone.amount,
                reference=str(milestone.pk)[:12],
                description="Milestone payment",
                callback_url=callback_url,
            )

            if result.get("ResponseCode") == "0":
                payment.mpesa_ref = result.get("CheckoutRequestID", "")
                payment.save()
                messages.success(
                    request,
                    f"M-Pesa prompt sent to {phone}. Enter your PIN to complete payment of KES {milestone.amount}.",
                )
                return redirect("client_contract_detail", pk=milestone.contract.pk)
            else:
                payment.status = "failed"
                payment.save()
                messages.error(request, f"M-Pesa error: {result.get('errorMessage', 'Unknown error')}.")

        except Exception as e:
            payment.status = "failed"
            payment.save()
            messages.error(request, f"Could not reach M-Pesa. Please try again. ({e})")

    return render(request, "payments/pay.html", {
        "milestone": milestone,
        "phone":     request.user.phone,
    })


@csrf_exempt
def mpesa_callback(request):
    if request.method != "POST":
        return JsonResponse({"status": "ok"})

    try:
        data     = json.loads(request.body)
        callback = data["Body"]["stkCallback"]
        code     = callback["ResultCode"]
        checkout = callback["CheckoutRequestID"]

        payment = Payment.objects.filter(mpesa_ref=checkout).first()
        if not payment:
            return JsonResponse({"status": "not found"})

        if code == 0:
            # Success — extract receipt
            items = {
                i["Name"]: i["Value"]
                for i in callback["CallbackMetadata"]["Item"]
            }
            payment.status         = "completed"
            payment.mpesa_receipt  = str(items.get("MpesaReceiptNumber", ""))
            payment.save()

            # Mark milestone as paid
            if payment.milestone:
                payment.milestone.status = "paid"
                payment.milestone.save()

        else:
            payment.status = "failed"
            payment.save()

    except Exception:
        pass

    return JsonResponse({"ResultCode": 0, "ResultDesc": "Accepted"})


@login_required
def pay_subscription(request):
    return render(request, "payments/subscription.html")


def mpesa_initiate(request):
    return JsonResponse({"status": "use /payments/milestone/<id>/pay/ instead"})
