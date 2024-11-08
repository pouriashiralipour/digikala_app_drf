# urls.py
from django.urls import path

from .views import OTPRequestView, OTPVerifyView, UserListView, UserMeView

urlpatterns = [
    path("auth/otp/request/", OTPRequestView.as_view(), name="otp_request"),
    path("auth/otp/verify/", OTPVerifyView.as_view(), name="otp_verify"),
    path("auth/users/", UserListView.as_view(), name="user_list"),
    path("auth/users/me/", UserMeView.as_view(), name="user_me"),
]
