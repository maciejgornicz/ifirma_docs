from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel, SecretStr
import yaml
from pathlib import Path
from typing import Self


class IFirmaSettings(BaseModel):
    """IFirma settings model"""
    url: str
    login: SecretStr
    password: SecretStr


class WebdriverSettings(BaseModel):
    """Webdriver settings model"""
    url: str


class AppSettings(BaseSettings):
    """Main settings model"""
    ifirma: IFirmaSettings
    webdriver: WebdriverSettings

    watched_dir: str
    heartbeat_timeout: int = 5
    model_config = SettingsConfigDict(env_nested_delimiter='__')

    @classmethod
    def from_yaml(cls, file_path: str) -> Self:
        """Class method to import settings from yaml file"""
        with open(file_path, 'r') as file:
            config = yaml.safe_load(file)
        return cls(**config)


path = str(Path(__file__).parent.parent)
settings: AppSettings = AppSettings.from_yaml(f'{path}/config/config.yaml')
