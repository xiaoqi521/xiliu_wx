# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import jpush
from jpush import common
from django.conf import settings

from celery import shared_task

jiguang_app_key = settings.JIGUANG_APP_KEY
jiguang_master_secret = settings.JIGUANG_MASTER_SECRET

ouch_push = jpush.JPush(jiguang_app_key, jiguang_master_secret)
ouch_push.set_logging("DEBUG")


@shared_task(queue='push_notification')
def to_all(content='', payload=None):
    push = ouch_push.create_push()
    push.audience = jpush.all_
    ios_data = {}
    android_data = {}

    if payload is None:
        pass
    else:
        ios_data['extras'] = payload
        android_data['extras'] = payload

    push.notification = jpush.notification(alert=content, ios=ios_data, android=android_data)
    push.platform = jpush.all_
    try:
        response = push.send()
    except common.Unauthorized:
        return 'Unauthorized', None
    except common.APIConnectionException:
        return 'Connection Error', None
    except common.JPushFailure:
        return 'Fail', None
    except:
        return 'Other Exception', None

    return None, response.status_code, response.payload


@shared_task(queue='push_notification')
def to_alias(alias=None, content='', payload=None):
    if not isinstance(alias, list):
        return 'Invalid Params', None

    if len(alias) == 0:
        return 'Empty Alias', None

    push = ouch_push.create_push()
    alias_arg = {"alias": alias}
    print(alias_arg)
    push.audience = jpush.audience(
        alias_arg
    )

    push.options = {
        "apns_production": True
    }

    ios_data = {}
    android_data = {}

    if payload is None:
        pass
    else:
        ios_data['extras'] = payload
        android_data['extras'] = payload

    push.notification = jpush.notification(alert=content, ios=ios_data, android=android_data)
    push.platform = jpush.all_
    try:
        response = push.send()
    except common.Unauthorized:
        return 'Unauthorized', None
    except common.APIConnectionException:
        return 'Connection Error', None
    except common.JPushFailure:
        return 'Fail', None
    except:
        return 'Other Exception', None

    return None, response.status_code, response.payload
