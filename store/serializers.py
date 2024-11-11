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

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", {})
        user = instance.user

        if "first_name" in user_data:
            user.first_name = user_data["first_name"]
        if "last_name" in user_data:
            user.last_name = user_data["last_name"]
        if "email" in user_data:
            user.email = user_data["email"]

        user.save()

        instance.birth_date = validated_data.get("birth_date", instance.birth_date)
        instance.save()

        return instance
