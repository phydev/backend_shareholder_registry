from rest_framework import routers

from .views import (
    me_view,
    user_view,
)

router = routers.DefaultRouter()
router.register(r"me", me_view.MeViewSet, basename="me")
router.register(r"user", user_view.UserModelViewSet, basename="user")
