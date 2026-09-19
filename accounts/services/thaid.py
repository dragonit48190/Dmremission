from authlib.common.security import generate_token
from authlib.integrations.django_client import OAuth
from django.conf import settings


oauth = OAuth()


def is_thaid_configured():
    """
    ตรวจสอบ Configuration ที่จำเป็นสำหรับ ThaID / OIDC
    """

    required_config = [
        settings.THAID_CLIENT_ID,
        settings.THAID_CLIENT_SECRET,
        settings.THAID_REDIRECT_URI,
        settings.THAID_SERVER_METADATA_URL,
    ]

    return all(required_config)


def get_thaid_client():
    """
    สร้าง OAuth/OIDC Client สำหรับ ThaID

    ใช้ OIDC Discovery / Server Metadata
    เพื่อให้ Authlib สามารถอ่านข้อมูล endpoint และ JWKS
    จากผู้ให้บริการได้
    """

    if not is_thaid_configured():
        return None

    client = oauth.create_client("thaid")

    if client is None:
        oauth.register(
            name="thaid",
            client_id=settings.THAID_CLIENT_ID,
            client_secret=settings.THAID_CLIENT_SECRET,
            server_metadata_url=settings.THAID_SERVER_METADATA_URL,
            client_kwargs={
                "scope": "openid",
            },
        )

        client = oauth.create_client("thaid")

    return client


def create_oidc_nonce():
    """
    สร้าง nonce สำหรับ OpenID Connect
    """
    return generate_token(32)