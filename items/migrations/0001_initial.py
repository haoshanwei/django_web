# Generated by Django 2.1.3 on 2019-10-12 01:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Items',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='项目名称', max_length=255, verbose_name='项目名称')),
                ('desc', models.CharField(help_text='项目简介', max_length=255, verbose_name='项目简介')),
                ('member', models.CharField(help_text='项目责任人', max_length=255, verbose_name='项目责任人')),
                ('createTime', models.DateField(auto_now=True, verbose_name='创建时间')),
                ('startTime', models.DateField(help_text='项目开始时间', verbose_name='项目开始时间')),
                ('endTime', models.DateField(help_text='项目结束时间', verbose_name='项目结束时间')),
            ],
            options={
                'verbose_name': '项目名称',
                'verbose_name_plural': '项目名称',
            },
        ),
        migrations.CreateModel(
            name='ItemsApplication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='板块名称,如龖藏App-User', max_length=255, verbose_name='板块名称')),
                ('desc', models.CharField(help_text='板块介绍', max_length=255, verbose_name='板块介绍')),
                ('member', models.CharField(help_text='板块测试负责人', max_length=255, verbose_name='板块测试负责人')),
                ('createTime', models.DateField(auto_now=True, verbose_name='创建时间')),
                ('Items', models.ForeignKey(help_text='项目名称', on_delete=django.db.models.deletion.CASCADE, to='items.Items')),
            ],
            options={
                'verbose_name': '板块名称',
                'verbose_name_plural': '板块名称',
            },
        ),
    ]
