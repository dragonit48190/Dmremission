from django.urls import path

from . import views
from . import views_thaid


app_name = "accounts"


urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile_view, name="profile"),
    path("avatar/", views.avatar_view, name="avatar"),

    # ThaID / OpenID Connect
    path(
        "thaid/login/",
        views_thaid.thaid_login_view,
        name="thaid_login",
    ),
    path(
        "thaid/callback/",
        views_thaid.thaid_callback_view,
        name="thaid_callback",
    ),
]