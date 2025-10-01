import logging
import time
from functools import partial, wraps
from pathlib import Path


def timer(func=None, *, level=logging.INFO, name=__file__):
    name = Path(name).name
    if func is None:
        return partial(timer, level=level, name=name)

    logging.basicConfig(encoding="utf-8", level=level)
    logger = logging.getLogger(name)

    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        value = func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        logger.log(level, f"Finished {func.__name__}() in {run_time:.4f} secs")
        return value

    return wrapper
