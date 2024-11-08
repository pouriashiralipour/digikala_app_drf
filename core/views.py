import random
import re

from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework import generics, permissions, status, views
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from core.models import CustomUser
from core.serializers import OTPRequestSerializer, OTPVerifySerializer, UserSerializer

User = get_user_model()


def is_phone_number(identifier):
    return re.match(r"^\+?\d{10,15}$", identifier) is not None


class IsAdminOrSelf(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj == request.user


class UserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return CustomUser.objects.all()
        return CustomUser.objects.filter(id=self.request.user.id)

    def perform_create(self, serializer):
        if self.request.user.is_staff:
            serializer.save()
        else:
            return Response({"detail": "Permission denied."}, status=403)


class UserMeView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class OTPRequestView(views.APIView):
    def post(self, request):
        serializer = OTPRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        identifier = serializer.validated_data["identifier"]

        if is_phone_number(identifier):
            otp = str(random.randint(10000, 99999))
            cache.set(f"otp_{identifier}", otp, 300)  # ذخیره OTP با انقضا 5 دقیقه
            cache.set(
                f"last_identifier_{request.user.id}", identifier, 300
            )  # ذخیره identifier برای کاربر
            print(f"OTP for {identifier}: {otp}")
        elif "@" in identifier:
            otp = str(random.randint(10000, 99999))
            cache.set(f"otp_{identifier}", otp, 300)
            cache.set(f"last_identifier_{request.user.id}", identifier, 300)
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

        otp = serializer.validated_data["otp"]
        identifier = cache.get(
            f"last_identifier_{request.user.id}"
        )  # بازیابی identifier از کش

        if not identifier:
            return Response(
                {"detail": "No identifier found for this session."},
                status=status.HTTP_400_BAD_REQUEST,
            )

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
