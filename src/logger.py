import logging
import logging.config
import structlog
from settings import settings


def configure_logger():
    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "plain": {
                    "()": structlog.stdlib.ProcessorFormatter,
                    "processor": structlog.processors.JSONRenderer(sort_keys=True),
                },
                "colored": {
                    "()": structlog.stdlib.ProcessorFormatter,
                    "processor": structlog.dev.ConsoleRenderer(colors=True),
                },
            },
            "handlers": {
                "default": {
                    "level": settings.LOG_LEGEL,
                    "class": "logging.StreamHandler",
                    "formatter": "colored",
                },
                "file": {
                    "level": logging.INFO,
                    "class": "logging.handlers.TimedRotatingFileHandler",
                    "filename": "kafka_performance.log",
                    "when": "d",
                    "backupCount": 3,
                    "formatter": "plain",
                },
            },
            "loggers": {
                "": {
                    "handlers": ["default", "file"],
                    "level": settings.LOG_LEGEL,
                    "propagate": True,
                },
            },
        }
    )
    structlog.configure(
        processors=[
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )


def get_logger(name: str) -> logging.Logger:
    return structlog.get_logger(name)
