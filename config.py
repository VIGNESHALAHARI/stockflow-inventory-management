import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")

    # Require a real secret key in production.
    if not SECRET_KEY:
        if os.getenv("APP_ENV", "development").lower() == "production":
            raise RuntimeError(
                "SECRET_KEY must be configured in production."
            )

        SECRET_KEY = "dev-only-secret-key-change-before-deployment"

    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "sqlite:///stockflow.db",
    )

    # Support PostgreSQL URLs from hosting providers.
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace(
            "postgres://",
            "postgresql://",
            1,
        )

    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"

    SESSION_COOKIE_SECURE = (
        os.getenv("SESSION_COOKIE_SECURE", "False").lower() == "true"
    )