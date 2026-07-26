from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.viewsets import ModelViewSet

from brreg.serializers.user_serializer import UserSerializer

from ..models.user import User


@extend_schema_view(
    list=extend_schema(
        summary="List users",
        description=(
            "Retrieve a list of users. Admin members can see all users, regular users can only see their own data."
        ),
        tags=["Users"],
    ),
    create=extend_schema(
        summary="Create user",
        description="Create a new user record. Requires authentication and appropriate permissions.",
        tags=["Users"],
    ),
    retrieve=extend_schema(
        summary="Get user",
        description="Retrieve a specific user by M-ID. Users can only access their own data unless they are admin.",
        tags=["Users"],
    ),
    update=extend_schema(
        summary="Update user",
        description="Update all fields of a specific user. Users can only update their own data unless they are admin.",
        tags=["Users"],
    ),
    partial_update=extend_schema(
        summary="Partially update user",
        description="Update specific fields of a user. Users can only update their own data unless they are admin.",
        tags=["Users"],
    ),
    destroy=extend_schema(
        summary="Delete user",
        description="Delete a specific user record. Requires appropriate permissions.",
        tags=["Users"],
    ),
)
class UserModelViewSet(ModelViewSet):
    """
    ViewSet for managing user entities.

    Actions:
    - list: Get all users (admin) or just self (regular users)
    - retrieve: Get a specific user (if admin or self)
    - update/partial_update: Update user details (if admin or self)

    All operations require authentication.
    Users can only access their own data unless they are admin members.
    """

    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "m_id"
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["email", "first_name", "last_name"]
    ordering_fields = ["email", "first_name", "last_name"]
    ordering = ["email"]
