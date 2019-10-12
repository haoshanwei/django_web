from django.db import models


# Create your models here.
# 项目表
class Items(models.Model):
	name = models.CharField('项目名称', max_length=255, help_text='项目名称')
	desc = models.CharField('项目简介', max_length=255, help_text='项目简介')
	member = models.CharField('项目责任人', max_length=255, help_text='项目责任人')
	createTime = models.DateField('创建时间', auto_now=True)
	startTime = models.DateField('项目开始时间', help_text='项目开始时间')
	endTime = models.DateField('项目结束时间', help_text='项目结束时间')

	class Meta:
		verbose_name = '项目名称'
		verbose_name_plural = '项目名称'

	def __str__(self):
		return self.name

# 项目-功能块表
class ItemsApplication(models.Model):
	Items = models.ForeignKey('Items', on_delete=models.CASCADE, help_text='项目名称')
	name = models.CharField('板块名称', max_length=255, help_text='板块名称,如龖藏App-User')
	desc = models.CharField('板块介绍', max_length=255, help_text='板块介绍')
	member = models.CharField('板块测试负责人', max_length=255, help_text='板块测试负责人')
	createTime = models.DateField('创建时间', auto_now=True)

	class Meta:
		verbose_name = '板块名称'
		verbose_name_plural = '板块名称'

	def __str__(self):
		return self.name




