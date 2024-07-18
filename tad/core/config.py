import logging
import secrets
from functools import lru_cache
from pathlib import Path
from typing import Any, TypeVar

from pydantic import (
    computed_field,
    model_validator,
)
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

from tad.core.exceptions import SettingsError
from tad.core.types import DatabaseSchemaType, EnvironmentType, LoggingLevelType

logger = logging.getLogger(__name__)

# Self type is not available in Python 3.10 so create our own with TypeVar
SelfSettings = TypeVar("SelfSettings", bound="Settings")

PROJECT_NAME: str = "TAD"
PROJECT_DESCRIPTION: str = "Transparency of Algorithmic Decision making"
VERSION: str = "0.1.0"  # replace in CI/CD pipeline


class Settings(BaseSettings):
    SECRET_KEY: str = secrets.token_urlsafe(32)

    ENVIRONMENT: EnvironmentType = "local"

    LOGGING_LEVEL: LoggingLevelType = "INFO"
    LOGGING_CONFIG: dict[str, Any] | None = None

    DEBUG: bool = False
    AUTO_CREATE_SCHEMA: bool = False

    CARD_DIR: Path = Path("/tmp/")  # TODO(berry): create better location for model cards  # noqa: S108

    # todo(berry): create submodel for database settings
    APP_DATABASE_SCHEME: DatabaseSchemaType = "sqlite"
    APP_DATABASE_DRIVER: str | None = None

    APP_DATABASE_SERVER: str = "db"
    APP_DATABASE_PORT: int = 5432
    APP_DATABASE_USER: str = "tad"
    APP_DATABASE_PASSWORD: str | None = None
    APP_DATABASE_DB: str = "tad"

    APP_DATABASE_FILE: str = "/database.sqlite3"

    model_config = SettingsConfigDict(extra="ignore")

    @computed_field
    def SQLALCHEMY_ECHO(self) -> bool:
        return self.DEBUG

    @computed_field
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        scheme: str = (
            f"{self.APP_DATABASE_SCHEME}+{self.APP_DATABASE_DRIVER}"
            if isinstance(self.APP_DATABASE_DRIVER, str)
            else self.APP_DATABASE_SCHEME
        )

        if self.APP_DATABASE_SCHEME == "sqlite":
            return f"{scheme}://{self.APP_DATABASE_FILE}"

        return str(
            MultiHostUrl.build(
                scheme=scheme,
                username=self.APP_DATABASE_USER,
                password=self.APP_DATABASE_PASSWORD,
                host=self.APP_DATABASE_SERVER,
                port=self.APP_DATABASE_PORT,
                path=self.APP_DATABASE_DB,
            )
        )

    @model_validator(mode="after")
    def _enforce_database_rules(self: SelfSettings) -> SelfSettings:
        if self.ENVIRONMENT == "production" and self.APP_DATABASE_SCHEME == "sqlite":
            raise SettingsError("APP_DATABASE_SCHEME")
        return self

    @model_validator(mode="after")
    def _enforce_debug_rules(self: SelfSettings) -> SelfSettings:
        if self.ENVIRONMENT == "production" and self.DEBUG:
            raise SettingsError("DEBUG")
        return self

    @model_validator(mode="after")
    def _enforce_autocreate_rules(self: SelfSettings) -> SelfSettings:
        if self.ENVIRONMENT == "production" and self.AUTO_CREATE_SCHEMA:
            raise SettingsError("AUTO_CREATE_SCHEMA")
        return self


# TODO(berry): make it a function with lrucache


@lru_cache(maxsize=8)
def get_settings() -> Settings:
    return Settings()
