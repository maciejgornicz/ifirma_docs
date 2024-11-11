"""Provide and initialize settings."""
from pydantic_settings import BaseSettings, SettingsConfigDict, PydanticBaseSettingsSource
from pydantic import BaseModel, SecretStr
import yaml
from pathlib import Path
from typing import Self, Tuple, Type


class IFirmaSettings(BaseModel):
    """IFirma settings model."""

    url: str
    login: SecretStr
    password: SecretStr


class WebdriverSettings(BaseModel):
    """Webdriver settings model."""

    url: str


class AppSettings(BaseSettings):
    """Main settings model."""

    ifirma: IFirmaSettings
    webdriver: WebdriverSettings

    watched_dir: str
    heartbeat_timeout: int
    model_config = SettingsConfigDict(env_nested_delimiter='__')

    @classmethod
    def from_yaml(cls, file_path: str) -> Self:
        """Import settings from yaml file."""
        with open(file_path, 'r') as file:
            config = yaml.safe_load(file)
        return cls(**config)

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        """Customize sources priority."""
        return env_settings, init_settings, dotenv_settings, file_secret_settings


path = str(Path(__file__).parent.parent)
settings: AppSettings = AppSettings.from_yaml(f'{path}/config/config.yaml')
