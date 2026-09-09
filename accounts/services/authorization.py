from accounts.models import RoleMapping
from accounts.services.hosxp import get_staff_by_cid


def authorize_staff_by_cid(cid):
    """
    ตรวจสอบสิทธิ์เข้า DM Remission จาก CID

    Flow:
    CID
      -> HOSxP staff
      -> groupname
      -> RoleMapping
      -> Django Group

    Default Deny:
    ถ้าไม่พบบุคลากร หรือไม่มี mapping หรือ mapping ถูกปิด
    จะไม่อนุญาตให้เข้าใช้งาน
    """

    staff = get_staff_by_cid(cid)

    if not staff:
        return {
            "allowed": False,
            "reason": "STAFF_NOT_FOUND",
            "staff": None,
            "django_group": None,
        }

    groupname = (staff.get("groupname") or "").strip()

    if not groupname:
        return {
            "allowed": False,
            "reason": "HOSXP_GROUP_NOT_FOUND",
            "staff": staff,
            "django_group": None,
        }

    role_mapping = (
        RoleMapping.objects
        .select_related("django_group")
        .filter(
            hosxp_groupname=groupname,
            is_active=True,
        )
        .first()
    )

    if not role_mapping:
        return {
            "allowed": False,
            "reason": "ROLE_NOT_ALLOWED",
            "staff": staff,
            "django_group": None,
        }

    return {
        "allowed": True,
        "reason": "AUTHORIZED",
        "staff": staff,
        "django_group": role_mapping.django_group,
    }