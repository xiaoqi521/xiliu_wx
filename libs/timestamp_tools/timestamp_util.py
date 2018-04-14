# coding=utf-8
from __future__ import division
import time
import dateutil.parser
import datetime


# Django imports
from rest_framework import serializers
from django.utils import timezone


# 使用 dateutil 来解析时间字符串, 转换成时间戳，如果出错返回 None
def str_to_standard_timestamp(raw_date_str):
    try:
        d = dateutil.parser.parse(raw_date_str)
    except:
        return None
    return time.mktime(d.timetuple()) + d.microsecond / 1e6


def str_to_datetime_obj(raw_date_str, tz=timezone.get_current_timezone()):
    try:
        d = dateutil.parser.parse(raw_date_str)
    except:
        return None
    return timezone.make_aware(d, tz)


# 获取 datetime 中的 date，并且添加时区信息
def datetime_to_date(dt):
    try:
        cur_dt = datetime.datetime.combine(timezone.localtime(dt).date(), datetime.datetime.min.time())
    except:
        return None

    return timezone.make_aware(cur_dt, timezone.get_current_timezone())


# 时间戳转换为标准的 YYYY-MM-DD HH:MM:SS 时间字符串，注意，此处是转为了 localtime！！！！！
def timestamp_to_format_str(timestamp=0.0):
    if timestamp < 0.0:
        timestamp = 0.0
    local_time = time.localtime(timestamp)
    str_time = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
    return str_time


def timestamp_to_datetime_obj(timestamp=0.0):
    if timestamp < 0.0:
        timestamp = 0.0
    local_time = datetime.datetime.fromtimestamp(timestamp)
    return timezone.make_aware(local_time, timezone.get_current_timezone())


def get_push_time(push_time):
    try:
        push_time_start = push_time[0]
        push_time_start = datetime.datetime.strptime(push_time_start, "%Y-%m-%d %H:%M:%S")
    except:
        push_time_start = timezone.datetime.now()

    try:
        push_time_end = push_time[1]
        push_time_end = datetime.datetime.strptime(push_time_end, "%Y-%m-%d %H:%M:%S")
    except:
        push_time_end = None  # forever
    return [push_time_start, push_time_end]


def is_one_week(dt, dt_other):
    # dt_other 大于 dt
    try:
        if dt and dt_other:
            diff_days = (dt_other - dt).days
            if diff_days == 0:
                return True
            if diff_days > 6:
                return False
            else:
                dt_week = dt.isoweekday()
                dt_other_week = dt_other.isoweekday()
                if dt_other_week > dt_week:
                    return True
                else:
                    return False
        else:
            return True
    except:
        return True


class NaiveDateTimeField(serializers.Field):
    def to_representation(self, value):
        try:
            naive_datetime = timezone.make_naive(value).strftime('%Y-%m-%d %H:%M:%S')
        except:
            return " "
        return naive_datetime


class TimeStampField(serializers.Field):
    def to_representation(self, value):
        try:
            timestamp = str_to_standard_timestamp(str(timezone.localtime(value)))
            timestamp = "%f" % float(timestamp)
        except:
            return "0"
        return timestamp


class TimeStampIntegerField(serializers.Field):
    def to_representation(self, value):
        try:
            timestamp = str_to_standard_timestamp(str(timezone.localtime(value)))
            timestamp = "%d" % int(timestamp)
        except:
            return "0"
        return timestamp


class DateTimeStampIntegerField(serializers.Field):
    def to_representation(self, value):
        try:
            timestamp = str_to_standard_timestamp(str(value))
            timestamp = "%f" % float(timestamp)
        except:
            return "0"
        return timestamp
