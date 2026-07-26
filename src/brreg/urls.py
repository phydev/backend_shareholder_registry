from django.urls import include, path

from . import router

app_name = "brreg"
urlpatterns = [
    path("v1/", include(router.router.urls)),
]
