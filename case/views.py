from django.shortcuts import render
from case.models import Apitest, Apistep, SingeApi
from items.models import Items
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.

# 单接口测试
@login_required
def api(request):
	username = request.session.get('user', '')
	api_list = SingeApi.objects.all()
	api_count = SingeApi.objects.all().count()
	paginator = Paginator(api_list, 10)  # 生成paginator对象,设置每页显示10条记录
	page = request.GET.get('page', 1)  # 获取当前的页码数,默认为第1页
	currentPage = int(page)  # 把获取的当前页码数转换成整数类型
	try:
		api_list = paginator.page(page)  # 获取当前页码数的记录列表
	except PageNotAnInteger:
		api_list = paginator.page(1)  # 如果输入的页数不是整数则显示第1页的内容
	except EmptyPage:
		api_list = paginator.page(paginator.num_pages)  # 如果输入的页数不在系统的页数中则显示最后一页的内容
	return render(request, 'api.html', {"user": username, "apis": api_list, 'apicount': api_count})


# 场景测试
@login_required
def scence_api(request):
	username = request.session.get('user', '')
	apitest_list = Apitest.objects.all()
	steps_list = Apistep.objects.all()
	apitest_count = Apitest.objects.all().count()  # 统计产品数
	paginator = Paginator(apitest_list, 10)  # 生成paginator对象,设置每页显示10条记录
	page = request.GET.get('page', 1)  # 获取当前的页码数,默认为第1页
	currentPage = int(page)  # 把获取的当前页码数转换成整数类型
	try:
		apitest_list = paginator.page(page)  # 获取当前页码数的记录列表
	except PageNotAnInteger:
		apitest_list = paginator.page(1)  # 如果输入的页数不是整数则显示第1页的内容
	except EmptyPage:
		apitest_list = paginator.page(paginator.num_pages)  # 如果输入的页数不在系统的页数中则显示最后一页的内容
	return render(request, "scence_api.html",
				  {"user": username, "apitests": apitest_list, "apitestcounts": apitest_count})  # 把值赋给apitestcounts这个变量


# 接口步聚管理
@login_required
def apistep_manage(request):
	username = request.session.get('user', '')
	apitestid = request.GET.get('apitest.id', None)
	apitest = Apitest.objects.get(id=apitestid)  # 获取所有接口测试用例
	apistep_list = Apistep.objects.all()
	return render(request, "apistep_manage.html", {"user": username, "apitest": apitest, "apisteps": apistep_list})


