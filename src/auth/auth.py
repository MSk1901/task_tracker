from fastapi_users.authentication import (AuthenticationBackend,
                                          CookieTransport, JWTStrategy)

from src.auth.config import settings

SECRET = settings.jwt_secret

cookie_transport = CookieTransport(cookie_max_age=3600, cookie_name='token')


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)
