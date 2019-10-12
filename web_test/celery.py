from __future__ import absolute_import
#!user/bin/python
#-*- coding: utf-8 -*-
__author__: 'huangsonglin@dcpai.cn'
__Time__: '2019/9/29 17:36'

import os
import sys
import django
from celery import Celery, platforms
from django.conf import settings

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web_test.settings')
django.setup()	# 注册到django

# 创建celery任务
app = Celery('web_test')
platforms.C_FORCE_ROOT = True
# 导入celery任务配置
app.config_from_object('django.conf:settings')
# 自动注册 celery任务
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
	print('Request: {0!r}'.format(self.request))