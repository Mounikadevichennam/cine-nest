import json
from typing import List, Any
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, AliasChoices, field_validator

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    DATABASE_URL: str = Field(
        default="sqlite:///./cinenest.db",
        validation_alias=AliasChoices("DATABASE_URL", "MYSQL_URL", "DATABASE_URI")
    )
    JWT_SECRET: str = Field(
        default="cinenest_super_secret_jwt_key_2026_change_in_production",
        validation_alias=AliasChoices("JWT_SECRET", "JWT_SECRET_KEY")
    )
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    TMDB_API_KEY: str = ""
    TMDB_BASE_URL: str = "https://api.themoviedb.org/3"
    CORS_ORIGINS: Any = Field(
        default=[
            "http://localhost:3000",
            "http://127.0.0.1:3000",
            "http://localhost:5173",
            "http://127.0.0.1:5173",
            "*"
        ],
        validation_alias=AliasChoices("CORS_ORIGINS", "FRONTEND_URL", "CLIENT_ORIGIN")
    )

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Any) -> List[str]:
        if isinstance(v, str):
            v = v.strip()
            if v.startswith("[") and v.endswith("]"):
                try:
                    parsed = json.loads(v)
                    if isinstance(parsed, list):
                        return [str(item).strip() for item in parsed]
                except Exception:
                    pass
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        elif isinstance(v, list):
            return [str(item).strip() for item in v]
        return ["*"]

settings = Settings()
