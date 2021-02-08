from typing import Optional
from queue import Queue
from threading import Thread
from kafka import KafkaProducer
from logger import get_logger
from settings import settings


class QueueProducer:

    MAX_BLOCK_MS = 100

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
        self._running = False
        self._queue = Queue(maxsize=settings.QSIZE)
        self._thread = Thread(target=self._read)
        self._use_flush = use_flush
        self._logger = get_logger(log_name or self.__class__.__name__)

    def start(self):
        self._running = True
        self._thread.start()

    def stop(self):
        self._running = False
        self._thread.join()

    def _read(self):
        while self._running:
            if not self._queue.empty():
                message = self._queue.get()
                self._logger.info(value=message, verb="GET", qsize=self._queue.qsize())
                self._producer.send(value=message, topic=self._topic)
                if self._use_flush:
                    self._producer.flush(timeout=100)

    def send(self, message: str):
        self._logger.info(value=message, verb="PUT", qsize=self._queue.qsize())
        self._queue.put(message)

    def _serializer(self, message: str):
        return message.encode()
