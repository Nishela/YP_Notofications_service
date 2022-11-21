import asyncio
import logging
from functools import wraps
from time import sleep


def sync(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return asyncio.get_event_loop().run_until_complete(func(*args, **kwargs))

    return wrapper


def backoff(start_sleep_time=0.1, factor=2, border_sleep_time=10):
    def func_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            n = 0
            while True:
                try:
                    return func(*args, **kwargs)
                except BaseException as e:
                    seconds = start_sleep_time * factor ** n
                    if seconds < border_sleep_time:
                        n += 1
                    else:
                        seconds = border_sleep_time
                    logging.error(f'{e}\nRetry after {seconds} seconds')
                    sleep(seconds)

        return inner

    return func_wrapper
