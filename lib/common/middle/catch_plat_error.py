# coding:utf-8
import re
from django.shortcuts import render, redirect
from django.http import HttpResponse

try:
    from django.utils.deprecation import MiddlewareMixin  # Django 1.10.x
except ImportError:
    MiddlewareMixin = object  # Django 1.4.x - Django 1.9.x


def catch_error_response(request, response):
    if response.status > 500:
        pass
    return response


# 1.11 中间件
# https://docs.djangoproject.com/en/1.11/topics/http/middleware/
# https://docs.djangoproject.com/en/1.11/ref/middleware/#middleware-ordering


class CatchPlatErrorMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 中间件响应前 增加自己的中间件
        response = self.get_response(request)

        ## 中间件响应后进行

        # 访客权限中间件
        response = catch_error_response(request=request, response=response)

        return response