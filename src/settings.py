import logging
from typing import List, Optional
from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    # Kafka
    KAFKA_HOST: str = "kafka-broker"
    KAFKA_PORT: int = 9092
    KAFKA_URL: Optional[str]
    KAFKA_TOPIC: str = "kafka-topic-1"

    # LogStash
    LOGSTASH_HOST: str = "logstash"
    LOGSTASH_PORT: int = 5000

    QSIZE: int = 100

    FILE_LOG_LEVEL = logging.INFO
    CONSOLE_LOG_LEVEL = logging.WARNING

    @validator("KAFKA_URL")
    def create_url(v, values, **kwargs):
        return f"{values.get('KAFKA_HOST')}:{values.get('KAFKA_PORT')}"


settings = Settings()
