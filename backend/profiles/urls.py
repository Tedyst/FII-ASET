from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from . import views

from .views import index

urlpatterns = [
    path("", index, name="index"),
    path("accounts/", include("allauth.urls")),  # allauth URLs
    path("accounts/mfa/", include("allauth.mfa.urls")),  # mfa URLs
    path(
        "upload-documents/", views.upload_documents, name="upload_documents"
    ),  # upload documents
]
