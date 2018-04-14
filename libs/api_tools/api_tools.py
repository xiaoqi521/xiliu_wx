# -*- coding: utf-8 -*-
from django.http import JsonResponse

from rest_framework import status
from rest_framework.response import Response


def generate_error_response(error_message, error_type):
    return Response({'retCode': error_message[0],
                     'retMsg': error_message[1]}, error_type)


def generate_ok_msg():
    return Response({'retCode': 0,
                     'retMsg': u"成功 | Success"}, status=status.HTTP_200_OK)


def generate_json_error_response(error_message, error_type):
    response_data = {'retCode': error_message[0],
                     'retMsg': error_message[1]}
    response = JsonResponse(response_data)

    response.status_code = error_type
    response.status_text = 'Bad Request'
    return response
