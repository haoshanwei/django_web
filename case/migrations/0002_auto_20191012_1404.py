# Generated by Django 2.1.3 on 2019-10-12 06:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('case', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='apitest',
            options={'ordering': ['id'], 'verbose_name': '场景测试', 'verbose_name_plural': '场景测试'},
        ),
        migrations.AlterModelOptions(
            name='singeapi',
            options={'ordering': ['id'], 'verbose_name': '接口信息', 'verbose_name_plural': '接口信息'},
        ),
    ]
