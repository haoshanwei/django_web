from django.db import models
from items.models import Items, ItemsApplication


# Create your models here.


class Apitest(models.Model):
	Items = models.ForeignKey('items.Items', on_delete=models.CASCADE, null=True)
	apitestname = models.CharField('流程名称', max_length=64)  # 流程接口测试场景
	apitestdesc = models.CharField('描述', max_length=64, null=True)  # 流程接口描述
	apitester = models.CharField('测试负责人', max_length=16)  # 执行人
	apitestresult = models.BooleanField('测试结果')  # 流程接口测试结果
	failreason = models.CharField('失败原因', max_length=5000, null=True, blank=True)  # 流程接口测试结果
	create_time = models.DateField('创建时间', auto_now=True)  # 创建时间，自动获取# 当前时间
	update_time = models.DateTimeField('更新时间', auto_now=True)  # 创建时间，自动获取# 当前时间

	class Meta:
		verbose_name = '场景测试'
		verbose_name_plural = '场景测试'


	def __str__(self):
		return self.apitestname


class Apistep(models.Model):
	Apitest = models.ForeignKey("Apitest", on_delete=models.CASCADE,)  # 关联接口 ID
	apistep = models.CharField('测试步聚', max_length=100, null=True)  # 测试步聚
	apiname = models.CharField('接口名称', max_length=100)  # 接口标题
	apiurl = models.CharField('url 地址', max_length=200)  # 地址
	apiheaders = models.CharField('请求头信息', max_length=1000, help_text='请写入json格式的数据.如果为空则填写"/"')  # 头信息
	apiparamvalue = models.CharField('请求参数和值', max_length=800, help_text='请写入json格式的数据.如果为空则填写"/"')  # 参数和值
	REQUEST_METHOD = (('get', 'get'), ('post', 'post'), ('put', 'put'), ('delete', 'delete'), ('patch', 'patch'))
	apimethod = models.CharField(verbose_name='请求方法', choices=REQUEST_METHOD, default='get', max_length=200, null=True)  # 请求方法
	apistatuscode = models.CharField('状态码', max_length=3)
	apiresult = models.CharField('预期结果', max_length=5000, help_text="多个校验时使用分号隔开.如name==admin;price=1")  # 预期结果
	apiresponse = models.TextField('响应结果', max_length=5000, null=True, blank=True)  # 响应结果
	apistatus = models.BooleanField('是否通过', null=True)  # 测试结果
	create_time = models.DateField('创建时间', auto_now=True)  # 创建时间，自动获# 取当前时间

	def __str__(self):
		return self.apistep

class SingeApi(models.Model):
	ItemsApplication = models.ForeignKey('items.ItemsApplication', on_delete=models.CASCADE)
	apiname = models.CharField('接口名称', max_length=100)  # 接口标题
	apidesc = models.CharField('接口描述|用途', max_length=100, help_text='接口描述|用途', null=True, blank=True)  # 接口标题
	apiurl = models.CharField('url 地址', max_length=1000)  # 地址
	apiheaders = models.CharField('请求头信息', max_length=1000, help_text='请求头信息;请写入json格式的数据.如果为空则填写"/"')  # 头信息
	apiparamvalue = models.CharField('请求参数和值', max_length=1000, help_text='请写入json格式的数据.如果为空则填写"/"')  # 参数和值
	REQUEST_METHOD = (('get', 'get'), ('post', 'post'), ('put', 'put'), ('delete', 'delete'), ('patch', 'patch'))
	apimethod = models.CharField(verbose_name='请求方法', choices=REQUEST_METHOD, default='post', max_length=200, null=True)  # 请求方法
	apistatuscode = models.CharField('状态码', max_length=3)
	apiresult = models.CharField('预期结果', max_length=5000, help_text="预期结果;多个校验时使用分号隔开.如name=admin;price=1")  # 预期结果
	apiresponse = models.TextField('响应结果', null=True, blank=True)  # 响应结果
	apistatus = models.BooleanField('是否通过')  # 测试结果
	create_time = models.DateField('创建时间', auto_now=True)  # 创建时间，自动获# 取当前时间
	update_time = models.DateField('执行时间', auto_now=True)  # 更新时间，自动获# 取当前时间1


	class Meta:
		verbose_name = '接口信息'
		verbose_name_plural = '接口信息'


	def __str__(self):
		return self.apiname