# coding=utf-8
import time
from base_cache import raw_redis_connection


def set_user_last_active_time_hash(user_id):
    redis_key = "useractivetime"
    user_id_key = str(user_id)
    raw_redis_connection.hset(redis_key, user_id_key, time.time())


def get_user_active_time():
    redis_key = "useractivetime"
    return raw_redis_connection.hgetall(redis_key)


def clear_user_last_active_time():
    redis_key = "useractivetime"
    return raw_redis_connection.delete(redis_key)
