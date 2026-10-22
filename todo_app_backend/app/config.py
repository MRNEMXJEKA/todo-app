from dataclasses import dataclass, field
import os

@dataclass(frozen=True)
class Settings:
    DATABASE_URL: str
    REDIS_URL: str
    cache_ttl_seconds: int = 3600
    cors_allowed_origin: list[str] = field(
        default_factory=lambda: ["http://localhost:3000"]
    )


def get_settings() -> Settings:
    return Settings(
        DATABASE_URL=os.getenv(
            "DATABASE_URL",
            "postgresql+psycopg://postgres:admin@127.0.0.1:5433/postgres",
        ),
        REDIS_URL=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
        cache_ttl_seconds=3600,
        cors_allowed_origin=["http://localhost:3000", "http://127.0.0.1:3000"],
        )
