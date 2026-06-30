import requests
import base64
import json
from datetime import datetime
from django.conf import settings


def get_mpesa_token():
    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    if getattr(settings, "MPESA_ENV", "sandbox") == "production":
        url = "https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

    key    = settings.MPESA_CONSUMER_KEY
    secret = settings.MPESA_CONSUMER_SECRET
    auth   = base64.b64encode(f"{key}:{secret}".encode()).decode()

    response = requests.get(url, headers={"Authorization": f"Basic {auth}"})
    return response.json().get("access_token")


def stk_push(phone, amount, reference, description, callback_url):
    token     = get_mpesa_token()
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    shortcode = settings.MPESA_SHORTCODE
    passkey   = settings.MPESA_PASSKEY
    password  = base64.b64encode(
        f"{shortcode}{passkey}{timestamp}".encode()
    ).decode()

    url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    if getattr(settings, "MPESA_ENV", "sandbox") == "production":
        url = "https://api.safaricom.co.ke/mpesa/stkpush/v1/processrequest"

    # Normalise phone: 07XX → 2547XX
    phone = str(phone).strip().replace(" ", "")
    if phone.startswith("0"):
        phone = "254" + phone[1:]
    elif phone.startswith("+"):
        phone = phone[1:]

    payload = {
        "BusinessShortCode": shortcode,
        "Password":          password,
        "Timestamp":         timestamp,
        "TransactionType":   "CustomerPayBillOnline",
        "Amount":            int(amount),
        "PartyA":            phone,
        "PartyB":            shortcode,
        "PhoneNumber":       phone,
        "CallBackURL":       callback_url,
        "AccountReference":  reference[:12],
        "TransactionDesc":   description[:13],
    }

    response = requests.post(
        url,
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )
    return response.json()
