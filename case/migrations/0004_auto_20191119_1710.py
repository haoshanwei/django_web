# Generated by Django 2.1.3 on 2019-11-19 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('case', '0003_auto_20191012_1412'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apistep',
            name='apiresponse',
            field=models.TextField(blank=True, max_length=5000, null=True, verbose_name='响应结果'),
        ),
        migrations.AlterField(
            model_name='singeapi',
            name='apiresponse',
            field=models.TextField(blank=True, null=True, verbose_name='响应结果'),
        ),
    ]
