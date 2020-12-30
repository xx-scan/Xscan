# coding:utf-8
from __future__ import absolute_import, unicode_literals

import subprocess
import os
from celery import shared_task, chain, chord


@shared_task
def exec_shell(shell):
    p = subprocess.Popen(shell, shell=True)
    import time
    time.sleep(1)
    os.waitpid(p.pid, os.W_OK)
    return {
        "stat": True,
        "cmd": shell,
        "reason": "远程执行命令执行成功！"
    }


@shared_task
def nmap_survive_scan(scantaskid):
    # 这里是基于UCP扫描的Scan
    return nmap_scan(nmap_args="-sU -T5 -sV --max-retries 1", scantaskid=scantaskid)


@shared_task
def nmap_result_import(args):
    pass
