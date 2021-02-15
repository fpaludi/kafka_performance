import logging
import logging.config
import structlog
import rapidjson
import logstash
from logstash import LogstashHandler
from settings import settings


def configure_logger():
    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "plain": {
                    # "()": structlog.stdlib.ProcessorFormatter,
                    "processor": structlog.processors.JSONRenderer(
                        sort_keys=True, serializer=rapidjson.dumps
                    ),
                },
                "colored": {
                    "()": structlog.stdlib.ProcessorFormatter,
                    "processor": structlog.dev.ConsoleRenderer(colors=True),
                },
            },
            "handlers": {
                "default": {
                    "level": settings.CONSOLE_LOG_LEVEL,
                    "class": "logging.StreamHandler",
                    "formatter": "colored",
                },
                "file": {
                    "level": settings.FILE_LOG_LEVEL,
                    "class": "logging.handlers.TimedRotatingFileHandler",
                    "filename": "kafka_performance.log",
                    "when": "d",
                    "backupCount": 3,
                    "formatter": "plain",
                },
                "logstash": {
                    "level": "INFO",
                    "class": "logstash.LogstashHandler",
                    "host": "logstash",
                    "port": 5000,
                    "version": 1,
                },
                "queue_listener": {
                    "class": "logger_queue_handler.QueueListenerHandler",
                    "handlers": [
                        "cfg://handlers.file",
                        "cfg://handlers.logstash",
                    ],
                },
            },
            "loggers": {
                "": {
                    "handlers": ["default", "queue_listener"],
                    "level": logging.INFO,
                    "propagate": False,
                },
            },
        }
    )
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            # structlog.stdlib.render_to_log_kwargs,
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )


def get_logger(name: str) -> logging.Logger:
    return structlog.get_logger(name)

