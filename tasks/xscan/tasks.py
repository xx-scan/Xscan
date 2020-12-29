# coding:utf-8
from __future__ import absolute_import, unicode_literals

import subprocess
import sys
import os
import django
from celery import shared_task, chain, chord
from lib.celery.decorator import register_as_period_task


def django_setup():
    DjangoModulePath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(DjangoModulePath)
    os.chdir(DjangoModulePath)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "website.settings")
    django.setup()


@shared_task
def push_cmd(cmd):
    p = subprocess.Popen(cmd, shell=True)
    import time
    time.sleep(1)
    os.waitpid(p.pid, os.W_OK)
    return {
        "stat": True,
        "cmd": cmd,
        "reason": "远程执行命令执行成功！"
    }
