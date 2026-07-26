from rest_framework import serializers

from brreg.models import User



class MeUserSerializer(serializers.ModelSerializer):
    """Serializer for user information in the me endpoint."""

    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "m_id", "is_active", "is_staff", "is_superuser"]
        read_only_fields = fields



class MeSerializer(serializers.Serializer):
    """
    Comprehensive serializer for the authenticated user's information.
    Returns user details, contact information, team memberships, and teams led.
    """

    user = MeUserSerializer(read_only=True)

