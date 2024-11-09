from pydantic_settings import BaseSettings
from pydantic import BaseModel, Field
import yaml


class IfirmaSettings(BaseModel):
    """IFirma settings model"""
    url: str = Field(alias='ifirma_url')
    login: str = Field(alias='ifirma_login')
    password: str = Field(alias='ifirma_password')


class WebdriverSettings(BaseModel):
    """Webdriver settings model"""
    host: str = Field(alias='webdriver_host')
    port: str = Field(alias='webdriver_port')


class Settings(BaseSettings):
    """Main settings model"""
    ifirma: IfirmaSettings
    webdriver: WebdriverSettings

    watched_dir: str = '/data'

    @classmethod
    def from_yaml(cls, file_path: str):
        """Class method to import settings from yaml file"""
        with open(file_path, 'r') as file:
            config = yaml.safe_load(file)
        return cls(**config)


settings = Settings.from_yaml('ifirma_docs/config/config.yaml')
