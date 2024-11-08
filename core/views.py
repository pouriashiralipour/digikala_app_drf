import random
import re

from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework import status, views
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from core.serializers import OTPRequestSerializer, OTPVerifySerializer

User = get_user_model()


def is_phone_number(identifier):
    return re.match(r"^\+?\d{10,15}$", identifier) is not None


class OTPRequestView(views.APIView):
    def post(self, request):
        serializer = OTPRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        identifier = serializer.validated_data["identifier"]

        if is_phone_number(identifier):
            otp = str(random.randint(10000, 99999))
            cache.set(f"otp_{identifier}", otp, 300)
            print(f"OTP for {identifier}: {otp}")
        elif "@" in identifier:
            otp = str(random.randint(10000, 99999))
            cache.set(f"otp_{identifier}", otp, 300)
            print(f"OTP for {identifier}: {otp}")
        else:
            return Response(
                {"detail": "Invalid identifier format."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response({"detail": "OTP sent successfully."}, status=status.HTTP_200_OK)


class OTPVerifyView(views.APIView):
    def post(self, request):
        serializer = OTPVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        identifier = serializer.validated_data["identifier"]
        otp = serializer.validated_data["otp"]

        cached_otp = cache.get(f"otp_{identifier}")
        if cached_otp != otp:
            return Response(
                {"detail": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST
            )

        if is_phone_number(identifier):
            user, created = User.objects.get_or_create(phone_number=identifier)
        else:
            user, created = User.objects.get_or_create(email=identifier)

        if created:
            user.identifier = identifier
            user.set_unusable_password()
            if is_phone_number(identifier):
                user.phone_number = identifier
            else:
                user.email = identifier
            user.save()

        refresh = RefreshToken.for_user(user)
        return Response(
            {"refresh": str(refresh), "access": str(refresh.access_token)},
            status=status.HTTP_200_OK,
        )
