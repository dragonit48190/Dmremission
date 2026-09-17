from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.templatetags.static import static
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from accounts.services.hosxp import get_staff_picture_by_cid

from .models import User


def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard:index")

    error_message = None

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        next_url = request.POST.get("next", "").strip()

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if (
            user is not None
            and user.auth_provider == User.AuthProvider.LOCAL
        ):
            login(request, user)

            if (
                next_url
                and url_has_allowed_host_and_scheme(
                    url=next_url,
                    allowed_hosts={request.get_host()},
                    require_https=request.is_secure(),
                )
            ):
                return redirect(next_url)

            return redirect("dashboard:index")

        error_message = "ชื่อผู้ใช้งานหรือรหัสผ่านไม่ถูกต้อง"

    return render(
        request,
        "accounts/login.html",
        {
            "error_message": error_message,
        },
    )


@require_POST
def logout_view(request):
    logout(request)
    return redirect("accounts:login")


@login_required
def profile_view(request):
    return render(
        request,
        "accounts/profile.html",
    )


@login_required
def avatar_view(request):
    user = request.user

    if not user.cid:
        return redirect(static("images/avatar-1.jpg"))

    picture = get_staff_picture_by_cid(user.cid)

    if not picture:
        return redirect(static("images/avatar-1.jpg"))

    if picture.startswith(b"\xff\xd8\xff"):
        content_type = "image/jpeg"

    elif picture.startswith(b"\x89PNG\r\n\x1a\n"):
        content_type = "image/png"

    else:
        return redirect(static("images/avatar-1.jpg"))

    response = HttpResponse(
        picture,
        content_type=content_type,
    )

    response["Cache-Control"] = "private, max-age=300"

    return response