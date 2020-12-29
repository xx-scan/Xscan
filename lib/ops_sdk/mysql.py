#!/usr/bin/env python
# -*-coding:utf-8-*-
'''
author : actanble
date   : 2018年2月5日13:37:54
role   : mysql操作
'''
import pymysql
from DBUtils.PooledDB import PooledDB

try:
    from ..xlogs import Log
    logging = Log(log_flag='pymysql_pool')
except Exception as e:
    import logging
    logging.error(e)

from ..configs import config_templates


class MysqlPool:

    config = {
        'creator': pymysql,
        'host': config_templates['MYSQL']['HOST'],
        'port': config_templates['MYSQL']['PORT'],
        'user': config_templates['MYSQL']['USER'],
        'password': config_templates['MYSQL']['PASSWD'],
        'db': config_templates['MYSQL']['NAME'],
        'charset': config_templates['MYSQL']['CHARSET'],
        'maxconnections': 70,
        'cursorclass': pymysql.cursors.DictCursor
    }
    pool = PooledDB(**config)

    def __enter__(self):
        self.conn = MysqlPool.pool.connection()
        self.cursor = self.conn.cursor()
        return self

    # 释放资源
    def __del__(self):
        self.cursor.close()
        self.conn.close()

    def __exit__(self, type, value, trace):
        self.cursor.close()
        self.conn.close()


def from_sql_get_data(sql):
    try:
        with MysqlPool() as db:
            db.cursor.execute(sql)
            res = db.cursor.fetchall()
    except Exception as e:
        logging.error("error", e)
        raise e
    return {"data": res}


def sql_action(sql):
    resnum = 0
    try:
        with MysqlPool() as db:
            resnum = db.cursor.execute(sql)
            db.conn.commit()
    except Exception as e:
        # 错误回滚
        logging.error("error", e)
        db.conn.rollback()
    return resnum