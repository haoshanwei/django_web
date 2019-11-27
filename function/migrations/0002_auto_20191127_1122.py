# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def forwards_func(apps, schema_editor):
    Function = apps.get_model("function", "Function")
    db_alias = schema_editor.connection.alias
    Function.objects.using(db_alias).bulk_create([
        Function(name="创建轰啪直播拍场", desc="创建超级主播的轰啪主播拍场"),
        Function(name="创建轰啪图文拍场", desc="创建轰啪图文拍场"),
        Function(name="创建轰啪卖家直播拍场", desc="创建轰啪卖家直播拍场"),
        Function(name="创建轰啪拍品", desc="创建轰啪拍品"),
        Function(name="创建秒啪拍品", desc="创建秒啪拍品"),
        Function(name="创建商城拍品-单品", desc="创建商城拍品-单品"),
        Function(name="创建商城拍品-多品", desc="创建商城拍品-多品"),
        Function(name="创建商城拍品-待价估询", desc="创建商城拍品-待价估询"),
        Function(name="账号注册", desc="账号注册"),
    ])


def reverse_func(apps, schema_editor):
    Function = apps.get_model("function", "Function")
    db_alias = schema_editor.connection.alias
    Function.objects.using(db_alias).filter(name="创建轰啪直播拍场").filter(desc="创建超级主播的轰啪主播拍场").delete()
    Function.objects.using(db_alias).filter(name="创建轰啪图文拍场").filter(desc="创建轰啪图文拍场").delete()
    Function.objects.using(db_alias).filter(name="创建轰啪卖家直播拍场").filter(desc="创建轰啪卖家直播拍场").delete()
    Function.objects.using(db_alias).filter(name="创建轰啪拍品").filter(desc="创建轰啪拍品").delete()
    Function.objects.using(db_alias).filter(name="创建秒啪拍品").filter(desc="创建秒啪拍品").delete()
    Function.objects.using(db_alias).filter(name="创建商城拍品-单品").filter(desc="创建商城拍品-单品").delete()
    Function.objects.using(db_alias).filter(name="创建商城拍品-多品").filter(desc="创建商城拍品-多品").delete()
    Function.objects.using(db_alias).filter(name="创建商城拍品-待价估询").filter(desc="创建商城拍品-待价估询").delete()
    Function.objects.using(db_alias).filter(name="账号注册").filter(desc="账号注册").delete()


class Migration(migrations.Migration):
    # 注明依赖的文件，一定要写
    dependencies = [
        ('function', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]