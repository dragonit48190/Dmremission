from authlib.integrations.base_client.errors import OAuthError

from django.conf import settings
from django.contrib.auth import login
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone

from accounts.services.provisioning import provision_user_from_cid
from accounts.services.thaid import (
    create_oidc_nonce,
    get_thaid_client,
    is_thaid_configured,
)


def thaid_login_view(request):
    """
    จุดเริ่มต้นการเข้าสู่ระบบด้วย ThaID
    """

    if not is_thaid_configured():
        return render(
            request,
            "accounts/login.html",
            {
                "error_message": (
                    "ระบบ ThaID ยังไม่ได้ตั้งค่าการเชื่อมต่อ"
                ),
            },
            status=503,
        )

    thaid = get_thaid_client()

    if thaid is None:
        return render(
            request,
            "accounts/login.html",
            {
                "error_message": (
                    "ไม่สามารถเตรียมการเชื่อมต่อ ThaID ได้"
                ),
            },
            status=503,
        )

    nonce = create_oidc_nonce()

    request.session["thaid_oidc_nonce"] = nonce

    redirect_uri = settings.THAID_REDIRECT_URI

    return thaid.authorize_redirect(
        request,
        redirect_uri,
        nonce=nonce,
    )


def thaid_callback_view(request):
    """
    Callback จาก ThaID / OpenID Connect
    """

    if not is_thaid_configured():
        return render(
            request,
            "accounts/login.html",
            {
                "error_message": (
                    "ระบบ ThaID ยังไม่ได้ตั้งค่าการเชื่อมต่อ"
                ),
            },
            status=503,
        )

    provider_error = request.GET.get("error")

    if provider_error:
        return render(
            request,
            "accounts/login.html",
            {
                "error_message": (
                    "ไม่สามารถยืนยันตัวตนด้วย ThaID ได้"
                ),
            },
            status=400,
        )

    thaid = get_thaid_client()

    if thaid is None:
        return render(
            request,
            "accounts/login.html",
            {
                "error_message": (
                    "ไม่สามารถเตรียมการเชื่อมต่อ ThaID ได้"
                ),
            },
            status=503,
        )

    try:
        token = thaid.authorize_access_token(request)

    except OAuthError:
        return render(
            request,
            "accounts/login.html",
            {
                "error_message": (
                    "การยืนยันตัวตน ThaID ไม่ถูกต้องหรือหมดอายุ"
                ),
            },
            status=400,
        )

    userinfo = token.get("userinfo")

    if not userinfo:
        return render(
            request,
            "accounts/login.html",
            {
                "error_message": (
                    "ThaID ไม่ส่งข้อมูลยืนยันตัวตนที่ระบบต้องการ"
                ),
            },
            status=400,
        )

    cid_claim = settings.THAID_CID_CLAIM

    if not cid_claim:
        return render(
            request,
            "accounts/login.html",
            {
                "error_message": (
                    "ระบบยังไม่ได้กำหนด Claim สำหรับ CID จาก ThaID"
                ),
            },
            status=503,
        )

    cid = str(userinfo.get(cid_claim, "")).strip()

    if not cid.isdigit() or len(cid) != 13:
        return render(
            request,
            "accounts/login.html",
            {
                "error_message": (
                    "ไม่พบข้อมูล CID ที่ถูกต้องจาก ThaID"
                ),
            },
            status=403,
        )

    result = provision_user_from_cid(cid)

    if not result["success"]:
        return render(
            request,
            "accounts/login.html",
            {
                "error_message": (
                    "บัญชีนี้ไม่ได้รับอนุญาตให้เข้าใช้งานระบบ"
                ),
            },
            status=403,
        )

    user = result["user"]

    user.last_identity_verified_at = timezone.now()
    user.save(
        update_fields=[
            "last_identity_verified_at",
            "updated_at",
        ]
    )

    login(
        request,
        user,
        backend="django.contrib.auth.backends.ModelBackend",
    )

    return redirect("dashboard:index")