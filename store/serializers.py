from rest_framework import serializers

from .models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    email = serializers.CharField(source="user.email")

    class Meta:
        model = Customer
        fields = ["id", "first_name", "last_name", "email", "birth_date"]
        read_only_fields = [
            "user",
        ]
