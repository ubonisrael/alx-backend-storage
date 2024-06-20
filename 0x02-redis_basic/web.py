#!/usr/bin/env python3
'''A module with tools for request caching and tracking.
'''
from datetime import timedelta
from functools import wraps
from typing import Callable
import redis
import requests


redis_store = redis.Redis()
'''The module-level Redis instance.
'''


def cacher(method: Callable) -> Callable:
    '''Caches the output of fetched data.
    '''
    @wraps(method)
    def wrapper(url) -> str:
        '''The wrapper function for caching the output.
        '''
        redis_store.incr(f'count:{url}')
        result = redis_store.get(f'result:{url}')
        if result:
            return result.decode('utf-8')
        result = method(url)
        redis_store.set(f'count:{url}', 0)
        redis_store.setex(f'result:{url}', timedelta(seconds=10), value=result)
        return result
    return wrapper


@cacher
def get_page(url: str) -> str:
    '''Returns the content of a URL after caching the request's response,
    and tracking the request.
    '''
    return requests.get(url).text
