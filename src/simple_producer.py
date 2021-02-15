from typing import Optional
from kafka import KafkaProducer
from logger import get_logger


class SimpleProducer:
    MAX_BLOCK_MS = 1000

    def __init__(
        self,
        url: str,
        topic: str,
        use_flush: bool = False,
        log_name: Optional[str] = None,
    ):
        self._producer = KafkaProducer(
            bootstrap_servers=url,
            max_block_ms=self.MAX_BLOCK_MS,
            value_serializer=self._serializer,
        )
        self._topic = topic
        self._use_flush = use_flush
        self._logger = get_logger(log_name or self.__class__.__name__)

    def send(self, message: str):
        self._producer.send(value=message, topic=self._topic)
        if self._use_flush:
            self._producer.flush(100)
        self._logger.info(
            value=message,
        )

    def _serializer(self, message: str):
        return message.encode()
