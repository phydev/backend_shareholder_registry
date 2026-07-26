from typing import Any

from rest_framework import serializers

from brreg.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["first_name", "last_name", "email", "m_id", "is_active"]
        model = User

    def create(self, validated_data: dict[str, Any]) -> User:
        """
        Special handling to create a user without a password,
        and set username to m_id, since username is required by AbstractUser.
        """
        validated_data["username"] = validated_data["m_id"]
        user = User.objects.create(**validated_data)
        return user
