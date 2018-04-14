# coding=utf-8

import time
import tokenlib

from django.conf import settings
from django.utils import timezone
from django.core.cache import cache

from rest_framework import exceptions
from rest_framework import authentication

from constants import error_constants, common_constants, user_constants

token_manager = tokenlib.TokenManager(secret=settings.ADMIN_SECRET_KEY,
                                      timeout=common_constants.TOKEN_EXPIRATION_TIME)


def generate_qrcode_token(user_id, expires):
    return token_manager.make_token({"userId": user_id, "expires": expires})


def get_qrcode_token_parsed(token, now):
    return token_manager.parse_token(str(token), now=now)


def generate_token(user_id, user_type):
    return token_manager.make_token({"userId": user_id, "userType": user_type})


def get_token_parsed(token, now):
    return token_manager.parse_token(str(token), now=now)


def get_token_expires_time(token):
    token_now = time.mktime(timezone.now().timetuple())
    cur_parsed_token = get_token_parsed(token, token_now)
    expires = cur_parsed_token['expires'] - token_now
    return expires


def token_in_blacklist(token):
    if cache.get(token):
        return True
    else:
        return False


def write_token_into_blacklist(token, key):
    expires = get_token_expires_time(token)
    try:
        cache.set(token, key, expires)
    except:
        return False
    return True


class Authentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        # 判断是不是debug模式
        # if settings.DEBUG:
        #      return None, None

        try:
            req_token = request.META['HTTP_AUTHORIZATION']
        except:
            raise exceptions.AuthenticationFailed(error_constants.ERR_TOKEN_ERROR)
        # 判断 get 还是 post
        if request.method == 'POST':
            req_user_id = request.POST.get('userId', '0')
        elif request.method == 'PUT':
            req_user_id = request.POST.get('userId', '0')
        elif request.method == 'DELETE':
            req_user_id = request.GET.get('userId', '0')
        elif request.method == 'GET':
            req_user_id = request.GET.get('userId', '0')
        else:
            req_user_id = request.query_params.get('userId', '0')

        # 验证token
        try:
            token_now = time.mktime(timezone.now().timetuple())
            cur_parsed_token = token_manager.parse_token(str(req_token), now=token_now)
            if int(req_user_id) != int(cur_parsed_token['userId']):
                raise exceptions.AuthenticationFailed(error_constants.ERR_TOKEN_ERROR)
            if token_in_blacklist(req_token):
                raise exceptions.AuthenticationFailed(error_constants.ERR_TOKEN_ERROR)
            if not cur_parsed_token['userType'] == user_constants.USER_TYPE_ADMIN:
                raise exceptions.AuthenticationFailed(error_constants.ERR_INVALID_USER_PRIVILEGE)
        except ValueError:
            raise exceptions.AuthenticationFailed(error_constants.ERR_TOKEN_ERROR)

        return cur_parsed_token, None
