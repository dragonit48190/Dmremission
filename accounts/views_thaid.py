from authlib.integrations.base_client.errors import OAuthError

from django.conf import settings
from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.http import require_GET

from accounts.services.provisioning import provision_user_from_cid
from accounts.services.thaid import (
    create_oidc_nonce,
    get_thaid_client,
    is_thaid_configured,
)


THAID_NONCE_SESSION_KEY = "thaid_oidc_nonce"


def _render_login_error(request, message, status):
    """
    แสดงหน้า Login พร้อมข้อความผิดพลาด
    โดยไม่เปิดเผยรายละเอียดภายในของ OAuth/OIDC
    """
    return render(
        request,
        "accounts/login.html",
        {
            "error_message": message,
        },
        status=status,
    )


def _clear_thaid_session(request):
    """
    ล้างข้อมูลชั่วคราวของ ThaID หลัง Callback
    """
    request.session.pop(THAID_NONCE_SESSION_KEY, None)


@require_GET
def thaid_login_view(request):
    """
    จุดเริ่มต้นการเข้าสู่ระบบด้วย ThaID / OpenID Connect
    """

    if request.user.is_authenticated:
        return redirect("dashboard:index")

    if not is_thaid_configured():
        return _render_login_error(
            request,
            "ระบบ ThaID ยังไม่ได้ตั้งค่าการเชื่อมต่อ",
            503,
        )

    thaid = get_thaid_client()

    if thaid is None:
        return _render_login_error(
            request,
            "ไม่สามารถเตรียมการเชื่อมต่อ ThaID ได้",
            503,
        )

    nonce = create_oidc_nonce()
    request.session[THAID_NONCE_SESSION_KEY] = nonce

    return thaid.authorize_redirect(
        request,
        settings.THAID_REDIRECT_URI,
        nonce=nonce,
    )


@require_GET
def thaid_callback_view(request):
    """
    Callback จาก ThaID / OpenID Connect

    ลำดับการทำงาน:
    1. ตรวจ configuration
    2. ตรวจ error จาก Identity Provider
    3. แลก Authorization Code เป็น Token
    4. ใช้ userinfo ที่ Authlib ตรวจสอบแล้ว
    5. ดึง CID จาก Claim ที่กำหนดจริง
    6. Provision ผู้ใช้กับ HOSxP / Django
    7. Login เข้า Django
    8. ล้างข้อมูลชั่วคราวใน session
    """

    if not is_thaid_configured():
        _clear_thaid_session(request)
        return _render_login_error(
            request,
            "ระบบ ThaID ยังไม่ได้ตั้งค่าการเชื่อมต่อ",
            503,
        )

    provider_error = request.GET.get("error")

    if provider_error:
        _clear_thaid_session(request)
        return _render_login_error(
            request,
            "ไม่สามารถยืนยันตัวตนด้วย ThaID ได้",
            400,
        )

    thaid = get_thaid_client()

    if thaid is None:
        _clear_thaid_session(request)
        return _render_login_error(
            request,
            "ไม่สามารถเตรียมการเชื่อมต่อ ThaID ได้",
            503,
        )

    expected_nonce = request.session.get(THAID_NONCE_SESSION_KEY)

    if not expected_nonce:
        return _render_login_error(
            request,
            "เซสชันการยืนยันตัวตน ThaID ไม่ถูกต้องหรือหมดอายุ",
            400,
        )

    try:
        token = thaid.authorize_access_token(request)

    except OAuthError:
        _clear_thaid_session(request)
        return _render_login_error(
            request,
            "การยืนยันตัวตน ThaID ไม่ถูกต้องหรือหมดอายุ",
            400,
        )

    userinfo = token.get("userinfo")

    if not userinfo:
        _clear_thaid_session(request)
        return _render_login_error(
            request,
            "ThaID ไม่ส่งข้อมูลยืนยันตัวตนที่ระบบต้องการ",
            400,
        )

    returned_nonce = userinfo.get("nonce")

    if returned_nonce and returned_nonce != expected_nonce:
        _clear_thaid_session(request)
        return _render_login_error(
            request,
            "ข้อมูลยืนยันตัวตน ThaID ไม่ถูกต้อง",
            400,
        )

    cid_claim = settings.THAID_CID_CLAIM

    if not cid_claim:
        _clear_thaid_session(request)
        return _render_login_error(
            request,
            "ระบบยังไม่ได้กำหนด Claim สำหรับ CID จาก ThaID",
            503,
        )

    cid = str(userinfo.get(cid_claim, "")).strip()

    if not cid.isdigit() or len(cid) != 13:
        _clear_thaid_session(request)
        return _render_login_error(
            request,
            "ไม่พบข้อมูล CID ที่ถูกต้องจาก ThaID",
            403,
        )

    result = provision_user_from_cid(cid)

    if not result["success"]:
        _clear_thaid_session(request)
        return _render_login_error(
            request,
            "บัญชีนี้ไม่ได้รับอนุญาตให้เข้าใช้งานระบบ",
            403,
        )

    user = result["user"]

    user.last_identity_verified_at = timezone.now()
    user.save(
        update_fields=[
            "last_identity_verified_at",
            "updated_at",
        ]
    )

    _clear_thaid_session(request)

    login(
        request,
        user,
        backend="django.contrib.auth.backends.ModelBackend",
    )

    return redirect("dashboard:index")
