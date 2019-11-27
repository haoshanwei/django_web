from django.db import models

# Create your models here.


class Function(models.Model):
	name = models.CharField("功能名字", max_length=20, null=False)
	desc = models.CharField("功能介绍", max_length=300, null=True)

	class Meta:
		verbose_name = '功能名字'
		verbose_name_plural = '功能名字'


	def __str__(self):
		return self.name