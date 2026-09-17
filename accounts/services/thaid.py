from authlib.common.security import generate_token
from authlib.integrations.django_client import OAuth
from django.conf import settings


oauth = OAuth()


def is_thaid_configured():
    """
    ตรวจสอบ Configuration ที่จำเป็นสำหรับ ThaID
    """

    required_config = [
        settings.THAID_CLIENT_ID,
        settings.THAID_CLIENT_SECRET,
        settings.THAID_AUTHORIZATION_URL,
        settings.THAID_TOKEN_URL,
        settings.THAID_ISSUER,
        settings.THAID_REDIRECT_URI,
    ]

    return all(required_config)


def get_thaid_client():
    """
    สร้าง OAuth/OIDC Client สำหรับ ThaID
    """

    if not is_thaid_configured():
        return None

    client = oauth.create_client("thaid")

    if client is None:
        oauth.register(
            name="thaid",
            client_id=settings.THAID_CLIENT_ID,
            client_secret=settings.THAID_CLIENT_SECRET,
            authorize_url=settings.THAID_AUTHORIZATION_URL,
            access_token_url=settings.THAID_TOKEN_URL,
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