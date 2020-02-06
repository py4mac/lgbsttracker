"""
The Background Common module.
Defines primitives for executing I/O blocking operations in the background using
a thread pool executor.
"""
import asyncio
import logging
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Callable

from lgbsttracker.utils import env

__all__ = [
    "run_async",
]


_logger = logging.getLogger()

db_thread_pool_executor_size = env.get_env("SQL_DB_THREAD_POOL_EXECUTOR_SIZE", 100)

###
# Thread pool executor used strictly to submit queries/operations to the database
# in background.
#
DB_THREAD_POOL_EXECUTOR = ThreadPoolExecutor(max_workers=db_thread_pool_executor_size, thread_name_prefix="db_worker_")


async def run_async(func: Callable[..., Any], *args, **kwargs) -> Any:
    """
    Runs a callable on the database thread pool executor using the current thread's
      I/O loop instance.
    Usage:
        def blocking_task(arg1, arg2, arg3):
            # ...
            # does some blocking stuff
            # ...
        run_async(blocking_task, arg1, arg2, arg3)
    :param Callable[..., Any] func: the function or callable to run in background
    :param tuple args: function arguments
    :param dict kwargs: function named arguments
    :return: func's return value
    """
    loop = asyncio.get_event_loop()

    def work():
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()

        if end - start > 5:
            try:
                query = args[0]
            except IndexError:
                query = args
            duration = "%.2f" % (end - start)
            _logger.warn("slow_query_logger: {duration}s for executing {query}".format(duration=duration, query=query))
        return result

    return await loop.run_in_executor(DB_THREAD_POOL_EXECUTOR, work)
