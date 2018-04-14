# coding=utf-8
from django.core.cache import cache
from django_redis import get_redis_connection
from libs.cache import cache_constants, base_cache

raw_redis_connection = get_redis_connection("default")


def cache_has_key(key):
    return cache.has_key(key)


def r_redis_delete_key(cur_key):
    try:
        raw_redis_connection.delete(cur_key)
    except:
        pass


def cache_key_value(cur_key='', cur_value='', timeout=cache_constants.CACHE_EXPIRE_TIMEOUT_5_MIN):
    if cur_key and cur_value:
        cache.set(cur_key, cur_value, timeout=timeout)
        return True
    return False


def cache_verify_sms_code(phone='', sms_code=''):

    get_sms_code = cache.get(phone)
    # print 'phone', phone
    # print 'sms_code', sms_code
    # print 'get_sms_code', get_sms_code
    if phone and sms_code and cache_has_key(phone):
        if get_sms_code == sms_code:
            # 验证通过删除sms code
            cur_key = ':1:' + phone
            r_redis_delete_key(cur_key)
            return True
    return False
