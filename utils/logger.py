import logging
import os


class WorkerFilter(logging.Filter):

    def filter(self, record):
        record.worker = os.environ.get("PYTEST_XDIST_WORKER", "main")
        return True

_LOG_FORMAT = "%(asctime)s | %(levelname)s | %(worker)s | %(name)s | %(message)s"
_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def get_logger(name="Framework"):

    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    worker_filter = WorkerFilter()
    formatter = logging.Formatter(_LOG_FORMAT, _DATE_FORMAT)

    # ===== File Handler =====
    worker_id = os.environ.get("PYTEST_XDIST_WORKER", "main")
    log_folder = "Logs"
    os.makedirs(log_folder, exist_ok=True)
    log_file = os.path.join(log_folder, f"test_{worker_id}.log")

    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    file_handler.addFilter(worker_filter)

    # ===== Stream Handler =====
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.addFilter(worker_filter)

    logger.addFilter(worker_filter)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger