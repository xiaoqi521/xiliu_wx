# coding=utf-8
import json
import random
import requests
from django.conf import settings
from django.utils.http import urlquote_plus
from celery import shared_task
from libs.sms.sms_cache import cache_verify_sms_code, cache_key_value, cache_has_key
from libs.sms import sms_constants
from libs.cache import cache_constants


@shared_task(queue='sms')
def send_sms(phone_number, content):
    if not cache_has_key(phone_number):
        print("Verify Code For %s Not Exist, Quit" % phone_number)
        return None

    if hasattr(settings, 'USE_ANJIEXIN_SMS_SERVICE'):
        rstr = "http://124.251.7.232:9007/axj_http_server/sms?name=liushui&pass=qwe321&mobiles="
        rstr += phone_number + "&content=" + urlquote_plus(content)
        res = requests.get(rstr)
    else:
        res = requests.post("https://sms.yunpian.com/v1/sms/send.json", data={
            'apikey': settings.SMS_API_KEY,
            'mobile': phone_number,
            'text': content
        })

    print("Send SMS To %s" % phone_number)
    print(content)
    print(res.text)


def verify_sms_code(phone='', sms_code=''):
    return cache_verify_sms_code(phone, sms_code)


def store_key_value(phone='', sms_code='', timeout=cache_constants.CACHE_EXPIRE_TIMEOUT_5_MIN):
    if phone in settings.SMS_WHITE_LIST:
        return cache_key_value(phone, '123456', timeout)
    # Anti - SMS Attack Fix
    cur_str_pos = phone.find(sms_constants.PREVENT_ATTACK_60_S)
    if not cur_str_pos == -1:
        cur_phone = phone[len(sms_constants.PREVENT_ATTACK_60_S) + cur_str_pos:]
        if cur_phone in settings.SMS_WHITE_LIST:
            return cache_key_value(phone, '123456', timeout)
    return cache_key_value(phone, sms_code, timeout)


def generate_sms_code(phone=''):
    return str(random.randint(100000, 1000000))


def send_sms_code_phone(phone='', sms_code=''):
    if phone and sms_code:
        cur_sms_content = "【科信智译】您的验证码是%s，为保障您的账户安全，请勿将验证码泄露他人，如非本人操作请勿理会。" % sms_code
        if not phone in settings.SMS_WHITE_LIST:
            send_sms.apply_async(args=[phone, cur_sms_content],
                                 queue=settings.SERVER_NAME + 'smsqueue',
                                 routing_key=settings.SERVER_NAME + 'smsqueuetasks')

        print('send sms code %s-%s', (phone, sms_code))


@shared_task()
def send_content(phone_number, content):
    if hasattr(settings, 'USE_ANJIEXIN_SMS_SERVICE'):
        rstr = "http://111.13.56.193:9007/axj_http_server/sms?name=liushui&pass=qwe321&mobiles="
        rstr += phone_number + "&content=" + urlquote_plus(content)
        res = requests.get(rstr)
    else:
        res = requests.post("https://sms.yunpian.com/v1/sms/send.json", data={
            'apikey': settings.SMS_API_KEY,
            'mobile': phone_number,
            'text': content
        })

    print("Send SMS To %s With Content %s" % (phone_number, content))
    print(res.text)


def send_context(phone='', sms_content=''):
    if phone and sms_content:
        if not (phone in settings.SMS_WHITE_LIST):
            send_content.apply_async(args=[phone, sms_content],
                                     queue=settings.SERVER_NAME + 'smsqueue',
                                     routing_key=settings.SERVER_NAME + 'smsqueuetasks')

        print('send context %s-%s', (phone, sms_content))
