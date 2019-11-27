# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def forwards_func(apps, schema_editor):
    Parameter = apps.get_model("parameter", "Parameter")
    db_alias = schema_editor.connection.alias
    Parameter.objects.using(db_alias).bulk_create([
        Parameter(value="http://train-h5.dcpai.cn/app/", name="host"),
        Parameter(value="""{'User-Agent':'Auction/5.0.0 (iPhone; iOS 11.4.1; Scale/2.00)',
          'Accept-Language':'zh-Hans-CN;q=1',
          'Connection':'keep-alive',
          'Content-Type':'application/x-www-form-urlencoded',
          'clientType':'IOS'}""", name="headers"),
        Parameter(value="dc_huangsonglin", name="web_admin"),
        Parameter(value="Aa123456", name="web_admin_password"),
        Parameter(value="http://train-h5.dcpai.cn", name="web_host_1"),
        Parameter(value="http://testadmin.dcpai.cn", name="web_host_2")
    ])


def reverse_func(apps, schema_editor):
    Parameter = apps.get_model("parameter", "Parameter")
    db_alias = schema_editor.connection.alias
    Parameter.objects.using(db_alias).filter(value="http://train-h5.dcpai.cn/app/").filter(name="host").delete()
    Parameter.objects.using(db_alias).filter(value="""{'User-Agent':'Auction/5.0.0 (iPhone; iOS 11.4.1; Scale/2.00)',
          'Accept-Language':'zh-Hans-CN;q=1',
          'Connection':'keep-alive',
          'Content-Type':'application/x-www-form-urlencoded',
          'clientType':'IOS'}""").filter(name="headers").delete()
    Parameter.objects.using(db_alias).filter(value="dc_huangsonglin").filter(name="web_admin").delete()
    Parameter.objects.using(db_alias).filter(value="Aa123456").filter(name="web_admin_password").delete()
    Parameter.objects.using(db_alias).filter(value="http://train-h5.dcpai.cn").filter(name="web_host_1").delete()
    Parameter.objects.using(db_alias).filter(value="http://testadmin.dcpai.cn").filter(name="web_host_2").delete()


class Migration(migrations.Migration):
    # 注明依赖的文件，一定要写
    dependencies = [
        ('parameter', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]