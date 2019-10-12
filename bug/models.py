from django.db import models
from items.models import Items, ItemsApplication
# Create your models here.

class Bug(models.Model):
	ItemsApplication = models.ForeignKey('items.ItemsApplication', on_delete=models.CASCADE, null=True)
	bugname = models.CharField('BUG名称', max_length=100, help_text='BUG名称')
	bugdesc = models.CharField('复现步骤', max_length=5000, help_text='复现步骤')
	bugimgFile = models.ImageField('BUG截图', max_length=100, help_text='BUG截图', null=True, blank=True, upload_to='image')
	BUG_STATUS = (('激活', '激活'), ('已解决', '已解决'), ('已关闭', '已关闭'), ('挂起', '挂起'))
	bugstatus = models.CharField(verbose_name='解决状态', choices=BUG_STATUS,
								 default='激活', max_length=200,null=True)# 解决状态
	BUG_LEVEL = (('1', '1'), ('2', '2'), ('3', '3'))
	buglevel = models.CharField(verbose_name='严重级别', choices=BUG_LEVEL,
								 default='2', max_length=200,null=True)
	bugcreater = models.CharField('BUG创建者', max_length=10)
	bugrepair = models.CharField('指派给', max_length=10)
	createtime = models.DateField('创建时间', auto_now=True)
	# closetime = models.DateField('关闭时间', auto_now=True)

	class Meta:
		verbose_name = 'BUG名称'
		verbose_name_plural = 'BUG名称'

	def __str__(self):
		return self.bugname

