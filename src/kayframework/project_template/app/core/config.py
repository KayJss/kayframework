from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SECRET_KEY: str = Field("CHANGE_ME", min_length=32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    DATABASE_URL: str = "sqlite:///users.db"
    ENV: str = "local"
    LOG_LEVEL: str = "INFO"
    MODULES: str = ""
    PLUGINS: str = ""
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:5173"

    COOKIE_NAME: str = "access_token"
    CSRF_COOKIE_NAME: str = "csrf_token"
    CSRF_HEADER_NAME: str = "X-CSRF-Token"
    COOKIE_SECURE: bool = True
    COOKIE_SAMESITE: str = "strict"
    COOKIE_DOMAIN: str | None = None
    COOKIE_PATH: str = "/"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

    def model_post_init(self, __context) -> None:
        if self.ENV.lower() == "local":
            self.COOKIE_SECURE = False


settings = Settings()
