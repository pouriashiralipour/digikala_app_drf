from djoser.serializers import UserCreateSerializer as DjoserUserCreateSerializer
from djoser.serializers import UserSerializer as DjoserUserSerializer
from rest_framework import serializers

from core.models import CustomUser


class UserCreateSerializer(DjoserUserCreateSerializer):
    class Meta(DjoserUserCreateSerializer.Meta):
        model = CustomUser
        fields = ["id", "phone_number", "email", "first_name", "last_name"]


class UserSerializer(DjoserUserSerializer):
    class Meta(DjoserUserSerializer.Meta):
        model = CustomUser
        fields = ["id", "phone_number", "email", "first_name", "last_name"]


class OTPRequestSerializer(serializers.Serializer):
    identifier = serializers.CharField()


class OTPVerifySerializer(serializers.Serializer):
    identifier = serializers.CharField()
    otp = serializers.CharField(max_length=5)
