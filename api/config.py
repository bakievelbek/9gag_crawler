import os

from dotenv import load_dotenv
from typing import Optional, Any
from pydantic import RedisDsn, validator
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    SPIDER_NAME: str = 'test_spider'
    REDIS_URI: Optional[RedisDsn] = None
    BASE_URL: str = {os.getenv('BASE_URL', 'https://9gag.com')}
    USER_URL: str = {os.getenv('USER_URL', 'https://9gag.com/u/')}

    # @validator("REDIS_URI", pre=True)
    # def assemble_db_connection(cls, v: Optional[str]) -> Any:
    #     if isinstance(v, str):
    #         return v
    #     return RedisDsn.build(
    #         scheme="redis",
    #         host=os.getenv('REDIS_HOST'),
    #         port=os.getenv('REDIS_PORT'),
    #         user=os.getenv('REDIS_USER'),
    #         password=os.getenv('REDIS_PASSWORD')
    #     )
    #
    class Config:
        case_sensitive = True


settings = Settings()
