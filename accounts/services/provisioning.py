from django.contrib.auth import get_user_model
from django.db import transaction

from accounts.models import UserRoleOverride
from accounts.services.authorization import authorize_staff_by_cid

User = get_user_model()


@transaction.atomic
def provision_user_from_cid(cid):
    """
    สร้างหรืออัปเดต Django User หลังผ่าน ThaID

    HOSxP = Source of Truth
    RoleMapping = Default Role
    UserRoleOverride = Manual Override
    Django = Authorization / Session / Audit
    """

    result = authorize_staff_by_cid(cid)

    if not result["allowed"]:
        return {
            "success": False,
            "reason": result["reason"],
            "user": None,
        }

    staff = result["staff"]
    default_group = result["django_group"]

    hosxp_loginname = staff["loginname"].strip()
    username = f"thaid_{hosxp_loginname.lower()}"

    user, created = User.objects.get_or_create(
        cid=cid,
        defaults={
            "username": username,
            "hosxp_loginname": hosxp_loginname,
            "auth_provider": User.AuthProvider.THAID,
            "is_active": True,
        },
    )

    changed = False

    if user.username != username:
        user.username = username
        changed = True

    if user.hosxp_loginname != hosxp_loginname:
        user.hosxp_loginname = hosxp_loginname
        changed = True

    if user.auth_provider != User.AuthProvider.THAID:
        user.auth_provider = User.AuthProvider.THAID
        changed = True

    if not user.is_active:
        user.is_active = True
        changed = True

    # ThaID user ห้ามใช้ Local Password
    if user.has_usable_password():
        user.set_unusable_password()
        changed = True

    if changed:
        user.save()

    # Manual Override มีสิทธิ์เหนือ HOSxP Mapping
    role_override = (
        UserRoleOverride.objects
        .select_related("django_group")
        .filter(
            user=user,
            is_active=True,
        )
        .first()
    )

    if role_override:
        effective_group = role_override.django_group
        role_source = "OVERRIDE"
    else:
        effective_group = default_group
        role_source = "HOSXP_MAPPING"

    # กำหนด Group ที่มีผลจริง
    user.groups.set([effective_group])

    return {
        "success": True,
        "reason": "PROVISIONED",
        "user": user,
        "created": created,
        "django_group": effective_group,
        "role_source": role_source,
        "staff": staff,
    }