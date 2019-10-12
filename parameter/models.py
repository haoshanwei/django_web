from django.db import models

# Create your models here.

class Parameter(models.Model):
	name = models.CharField('参数名字', max_length=20, help_text='参数名字', null=False)
	value = models.CharField('参数值', max_length=500, help_text='设置参数的值', null=False)
	createTime = models.DateField('创建时间', auto_now=True)

	class Meta:
		verbose_name = '参数信息'
		verbose_name_plural = '参数信息'

	def __str__(self):
		return self.name