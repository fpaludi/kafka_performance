from time import perf_counter, sleep
from uuid import uuid4
from simple_producer import SimpleProducer
from queue_producer import QueueProducer
from settings import settings
from logger import configure_logger, get_logger

configure_logger()


N_MSGS = 10_000


def main():
    logger = get_logger("MAIN")
    # -----------------------
    # Simple Producer
    # -----------------------
    simple_producer = SimpleProducer(
        settings.KAFKA_URL, "simple_prod", log_name="SimpleProducer"
    )
    t0 = perf_counter()
    for _ in range(N_MSGS):
        simple_producer.send(str(uuid4()))
    t1 = perf_counter()
    logger.warning(f"Simple Time: {t1 - t0}")

    # -----------------------
    # Simple Producer w Flush
    # -----------------------
    simple_producer = SimpleProducer(
        settings.KAFKA_URL,
        "simple_prod",
        use_flush=True,
        log_name="SimpleFlushProducer",
    )
    t0 = perf_counter()
    for _ in range(N_MSGS):
        simple_producer.send(str(uuid4()))
    t1 = perf_counter()
    logger.warning(f"Flush Time: {t1 - t0}")

    # -----------------------
    # Queue/Sync Producer
    # -----------------------
    queue_producer = QueueProducer(
        settings.KAFKA_URL, "queue_prod", log_name="QueueProducer"
    )
    queue_producer.start()
    sleep(1)
    t0 = perf_counter()
    for _ in range(N_MSGS):
        queue_producer.send(str(uuid4()))
    t1 = perf_counter()
    logger.warning(f"Queue Time: {t1 - t0}")
    sleep(1)
    queue_producer.stop()

    # -----------------------
    # Queue/Sync Producer w flush
    # -----------------------
    queue_flush_producer = QueueProducer(
        settings.KAFKA_URL,
        "queue_prod",
        use_flush=True,
        log_name="QueueFlushProducer",
    )
    queue_flush_producer.start()
    sleep(1)
    t0 = perf_counter()
    for _ in range(N_MSGS):
        queue_flush_producer.send(str(uuid4()))
    t1 = perf_counter()
    logger.warning(f"Queue Flush Time: {t1 - t0}")
    sleep(1)
    queue_flush_producer.stop()


if __name__ == "__main__":
    main()
