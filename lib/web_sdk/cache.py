#!/usr/bin/env python
# -*-coding:utf-8-*-
"""
Author : actanble
date   : 2018年4月11日
role   : 缓存
"""

import base64
import json
# from .consts import const

import redis
from shortuuid import uuid
from libs.ops_sdk.tools import singleton, convert
from libs.conf import config


@singleton
class Cache(object):
    def __init__(self):
        self.__redis_connections = {}

        auth = config.RD_HOST
        host = config.RD_HOST
        port = config.RD_PORT
        db = config.RD_DB
        return_utf8 = False
        if config.RD_DECODE_RESPONSES:
            return_utf8 = config.RD_DECODE_RESPONSES
        password = config.RD_PASSWORD

        if auth:
            redis_conn = redis.Redis(host=host, port=port, db=db, password=password, decode_responses=return_utf8)
        else:
            redis_conn = redis.Redis(host=host, port=port, db=db, decode_responses=return_utf8)
        self.__redis_connection = redis_conn
        self.__salt = str(uuid())

    def set(self, key, value, expire=-1, private=True, pipeline=None):
        real_key = self.__get_key(key, private)
        execute_main = self.__get_execute_main(pipeline)
        if expire > 0:
            execute_main.set(real_key, value, ex=expire)
        else:
            execute_main.set(real_key, value)

    def set_json(self, key, value, expire=-1,  private=True, pipeline=None):
        value = json.dumps(value)
        value = base64.b64encode(value.encode('utf-8'))
        self.set(key, value, expire, private, pipeline)

    def get(self, key, default='', private=True, pipeline=None):
        real_key = self.__get_key(key, private)
        execute_main = self.__get_execute_main(pipeline)
        if execute_main.exists(real_key):
            result = execute_main.get(real_key)
            # TODO 2018/11/4 修复了 `deocde\encode` 问题;
            return result
        return default

    def incr(self, key, private=True, amount=1):
        real_key = self.__get_key(key, private)
        execute_main = self.__get_execute_main( None)
        if execute_main.exists(real_key):
            execute_main.incr(real_key, amount=amount)
            return self.get(key, default='0', private=private)
        return None

    def get_json(self, key, default='', private=True):
        result = self.get(key, default, private)
        result = str(base64.b64decode(result), encoding='utf-8')
        if result:
            result = json.loads(result)
        return result

    def delete(self, *keys,  private=True, pipeline=None):
        execute_main = self.__get_execute_main( pipeline)
        _keys = [self.__get_key(key, private) for key in keys]
        return execute_main.delete(*_keys)

    def clear(self):
        execute_main = self.__get_execute_main(None)
        execute_main.flushdb()

    def get_pipeline(self):
        return self.__redis_connection.pipeline()

    def execute_pipeline(self, pipeline):
        if pipeline:
            return pipeline.execute()

    def get_conn(self):
        return self.__get_execute_main()

    def hgetall(self, key, default='',  private=True):
        real_key = self.__get_key(key, private)
        execute_main = self.__get_execute_main(None)
        if execute_main.exists(real_key):
            result = execute_main.hgetall(real_key)
            result = convert(result)
        else:
            return default
        return result

    @property
    def redis(self):
        return self.__get_execute_main()

    def __get_key(self, key, private=True):
        if private:
            return '%s%s' % (self.__salt, key)
        else:
            return key

    def __get_execute_main(self, pipeline=None):
        if pipeline:
            return pipeline
        return self.__redis_connection


def get_cache():
    return Cache()
