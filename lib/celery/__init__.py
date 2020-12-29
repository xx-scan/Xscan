# -*- coding: utf-8 -*-

import os
import sys
from datetime import timedelta
from celery import Celery, platforms
from celery.schedules import crontab

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.insert(PROJECT_DIR)

# Todo: Set ENV and autodiscover_tasks based in django-beat ;
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.settings')

cel = Celery('Scanner')
platforms.C_FORCE_ROOT = True

cel.conf.timezone = 'Asia/Shanghai'
cel.conf.enable_utc = False

cel.conf.beat_schedule = {
    # 名字随意命名
    'add-every-10-seconds': {
        # 执行tasks1下的test_celery函数
        'task': 'celery_task.tasks1.test_celery',
        'schedule': timedelta(seconds=2),
        # 传递参数
        'args': ('test',)
    },
    'add-every-12-seconds': {
        'task': 'celery_task.tasks1.test_celery',
        'schedule': crontab(minute=42, hour=8, day_of_month=11, month_of_year=4),
        'args': (16, 16)
    },
}

from web import settings

configs = {k: v for k, v in settings.__dict__.items() if k.startswith('CELERY')}
cel.namespace = 'CELERY'
cel.conf.update(configs)

# TODO 老版本寻找 website下的 task
# cel.autodiscover_tasks(lambda: [app_config.split('.')[0] for app_config in settings.INSTALLED_APPS])

# TODO 2020-12-29 新版本统一从tasks目录下寻找
cel.autodiscover_tasks('tasks')
