from django.contrib import admin
from django.urls import include, path

from dashboard import public_views


urlpatterns = [
    # Public Legal Pages
    path(
        "privacy/",
        public_views.privacy_policy,
        name="privacy_policy",
    ),
    path(
        "terms/",
        public_views.terms_of_use,
        name="terms_of_use",
    ),

    path("admin/", admin.site.urls),

    path(
        "accounts/",
        include("accounts.urls"),
    ),

    path(
        "",
        include("dashboard.urls"),
    ),
]