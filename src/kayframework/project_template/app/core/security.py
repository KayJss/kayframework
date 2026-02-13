from datetime import datetime, timedelta, timezone
import secrets
from fastapi import HTTPException, Response, status
from jose import JWTError, ExpiredSignatureError, jwt
from passlib.context import CryptContext

from app.core.config import settings


class Security:
    _pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @staticmethod
    def hash_password(password: str) -> str:
        return Security._pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return Security._pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def _require_secret_key() -> str:
        if settings.SECRET_KEY == "CHANGE_ME" or len(settings.SECRET_KEY) < 32:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Server configuration error.",
            )
        return settings.SECRET_KEY

    @staticmethod
    def create_csrf_token() -> str:
        return secrets.token_urlsafe(32)

    @staticmethod
    def create_access_token(subject: str, csrf_token: str, expires_delta: timedelta | None = None) -> str:
        now = datetime.now(timezone.utc)
        expire = now + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode = {
            "sub": subject,
            "exp": expire,
            "iat": now,
            "csrf": csrf_token,
            "type": "access",
        }
        return jwt.encode(to_encode, Security._require_secret_key(), algorithm=settings.ALGORITHM)

    @staticmethod
    def decode_access_token(token: str) -> dict:
        try:
            payload = jwt.decode(
                token,
                Security._require_secret_key(),
                algorithms=[settings.ALGORITHM],
                options={"verify_aud": False},
            )
        except ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token süresi doldu.")
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Geçersiz token.")
        return payload

    @staticmethod
    def set_auth_cookies(response: Response, access_token: str, csrf_token: str) -> None:
        max_age = settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        response.set_cookie(
            key=settings.COOKIE_NAME,
            value=access_token,
            httponly=True,
            secure=settings.COOKIE_SECURE,
            samesite=settings.COOKIE_SAMESITE,
            domain=settings.COOKIE_DOMAIN,
            path=settings.COOKIE_PATH,
            max_age=max_age,
        )
        response.set_cookie(
            key=settings.CSRF_COOKIE_NAME,
            value=csrf_token,
            httponly=False,
            secure=settings.COOKIE_SECURE,
            samesite=settings.COOKIE_SAMESITE,
            domain=settings.COOKIE_DOMAIN,
            path=settings.COOKIE_PATH,
            max_age=max_age,
        )

    @staticmethod
    def clear_auth_cookies(response: Response) -> None:
        response.delete_cookie(key=settings.COOKIE_NAME, domain=settings.COOKIE_DOMAIN, path=settings.COOKIE_PATH)
        response.delete_cookie(key=settings.CSRF_COOKIE_NAME, domain=settings.COOKIE_DOMAIN, path=settings.COOKIE_PATH)
