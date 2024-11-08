# urls.py
from django.urls import path

from core.views import OTPRequestView, OTPVerifyView

urlpatterns = [
    path("auth/otp/request/", OTPRequestView.as_view(), name="otp_request"),
    path("auth/otp/verify/", OTPVerifyView.as_view(), name="otp_verify"),
]
