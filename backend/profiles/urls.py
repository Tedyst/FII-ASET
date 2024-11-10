from django.urls import include, path

from .views import index

urlpatterns = [
    path("", index, name="index"),
    path("accounts/", include("allauth.urls")),  # allauth URLs
    path("accounts/mfa/", include("allauth.mfa.urls")),  # mfa URLs
]
