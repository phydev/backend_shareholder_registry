from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from brreg.serializers.me_serializer import MeSerializer


@extend_schema_view(
    list=extend_schema(
        summary="Get current user information",
        description=(
            "Retrieve comprehensive information about the authenticated user, including:\n"
            "- User profile (email, name, m_id)\n"
            "- Associated contact (if any)\n"
            "- Team memberships\n"
            "- Teams where the user's contact is a leader\n"
            "- Registry roles and access\n\n"
            "By default, only active team memberships are returned (where valid_to is null). "
            "Use `include_inactive=true` to include inactive memberships."
        ),
        parameters=[
            OpenApiParameter(
                name="include_inactive",
                description="Include inactive team memberships (where valid_to is not null)",
                required=False,
                type=bool,
                default=False,
            ),
        ],
        tags=["Current User"],
    ),
)
class MeViewSet(ViewSet):
    """
    ViewSet for retrieving authenticated user information.
    Read-only endpoint that returns user, contact, and team information.
    """

    serializer_class = MeSerializer

    def list(self, request: Request) -> Response:
        """
        Get information about the authenticated user.

        Returns user details, contact information, team memberships, and teams led.
        """
        user = request.user
        contact = None


        data = {
            "user": user,
            "contact": contact,
        }

        serializer = MeSerializer(data)
        return Response(serializer.data)
