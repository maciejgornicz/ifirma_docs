from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel, SecretStr
import yaml


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

    watched_dir: str = '/data'

    model_config = SettingsConfigDict(env_nested_delimiter='__')

    @classmethod
    def from_yaml(cls, file_path: str):
        """Class method to import settings from yaml file"""
        with open(file_path, 'r') as file:
            config = yaml.safe_load(file)
        return cls(**config)


settings = AppSettings.from_yaml('ifirma_docs/config/config.yaml')
