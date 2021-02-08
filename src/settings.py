import logging
from typing import List, Optional
from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    KAFKA_HOST: str = "kafka-broker"
    KAFKA_PORT: int = 9092
    KAFKA_URL: Optional[str]
    KAFKA_TOPIC: str = "kafka-topic-1"

    QSIZE = 100

    LOG_LEGEL = logging.INFO

    @validator("KAFKA_URL")
    def create_url(v, values, **kwargs):
        return f"{values.get('KAFKA_HOST')}:{values.get('KAFKA_PORT')}"


settings = Settings()
