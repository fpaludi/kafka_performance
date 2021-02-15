from logging.config import ConvertingList
from logging.handlers import QueueHandler, QueueListener
from queue import Queue
from atexit import register


def _resolve_handlers(handlers):
    if not isinstance(handlers, ConvertingList):
        return handlers
    return [handlers[i] for i in range(len(handlers))]


class QueueListenerHandler(QueueHandler):
    def __init__(
        self, handlers, respect_handler_level=True, auto_run=True
    ):
        queue=Queue(-1)  # Infinite Queue
        super().__init__(queue)
        handlers = _resolve_handlers(handlers)
        self._listener = QueueListener(
            self.queue, *handlers, respect_handler_level=respect_handler_level
        )
        if auto_run:
            self.start()
            register(self.stop)

    def start(self):
        self._listener.start()

    def stop(self):
        self._listener.stop()

    def emit(self, record):
        return super().emit(record)

