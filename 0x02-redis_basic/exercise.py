#!/usr/bin/env python3
"""contains the Cache class"""
import random
import redis
import uuid
from functools import wraps
from typing import Union, Callable


Def = Union[str, int, float, bytes]


def count_calls(method: Callable) -> Callable:
    """count how many times methods of the Cache class are called"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        returns the given method after
        incrementing the number of times called
        """
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """store the history of inputs and outputs for a particular function"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        append ":inputs" and ":outputs" to the decorated function's
        qualified name to create input and output list keys, respectively.
        """
        name = method.__qualname__
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush("{}:inputs".format(name), str(args))
        output = method(self, *args, **kwargs)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush("{}:outputs".format(name), output)
        return output
    return wrapper


def replay(func: Callable) -> None:
    """display the history of calls of a particular function"""
    if func is None or not hasattr(func, '__self__'):
        return
    redis_store = getattr(func.__self__, '_redis', None)
    if not isinstance(redis_store, redis.Redis):
        return
    func_name = func.__qualname__
    in_key = '{}:inputs'.format(func_name)
    out_key = '{}:outputs'.format(func_name)
    func_call_count = 0
    if redis_store.exists(func_name) != 0:
        func_call_count = int(redis_store.get(func_name))
    print('{} was called {} times:'.format(func_name, func_call_count))
    func_inputs = redis_store.lrange(in_key, 0, -1)
    func_outputs = redis_store.lrange(out_key, 0, -1)
    for func_input, func_output in zip(func_inputs, func_outputs):
        print('{}(*{}) -> {}'.format(
            func_name, func_input.decode("utf-8"),
            func_output,
        ))


class Cache:
    """class to be used for caching requests"""
    def __init__(self) -> None:
        """initializes a Cache instance"""
        self._redis: redis.Redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Def) -> str:
        """takes a data argument and returns a string"""
        key: str = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None) -> Def:
        """retrieves a value associated with a key"""
        if fn is None:
            return self._redis.get(key)
        return fn(self._redis.get(key))
