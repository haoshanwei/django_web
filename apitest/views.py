import pymysql
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from items.models import Items, ItemsApplication
from case.models import SingeApi, Apitest, Apistep
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from djcelery.models import PeriodicTask, CrontabSchedule, IntervalSchedule
from .tasks import *


# Create your views here.
@login_required
def task_apis(request):
	api_test.delay()
	username = request.session.get('user', '')
	apis_list = SingeApi.objects.all()
	apis_count = SingeApi.objects.all().count()  # 统计接口数
	db = pymysql.connect(user='root', db='web', passwd='root', host='192.168.10.37')
	cursor = db.cursor()
	rightsql = 'SELECT count(id) FROM case_singeapi WHERE apistatus=TRUE'
	rightresult = cursor.execute(rightsql)
	apis_pass_count = [row[0] for row in cursor.fetchmany(rightresult)][0]
	worngsql = 'SELECT count(id) FROM case_singeapi WHERE apistatus=FALSE'
	wrongresult = cursor.execute(worngsql)
	apis_fail_count = [row[0] for row in cursor.fetchmany(wrongresult)][0]
	db.close()
	return render(request, "task_api_report.html",
				  {"user": username, "apis": apis_list, "apiscounts": apis_count, "apis_pass_counts": apis_pass_count,
				   "apis_fail_counts": apis_fail_count})  # 把值赋给apiscounts 变量

@login_required
def task_apisteps(request):
	scence_test()
	username = request.session.get('user', '')
	apis_list = Apitest.objects.all()
	apis_count = Apitest.objects.all().count()  # 统计接口数
	db = pymysql.connect(user='root', db='web', passwd='root', host='192.168.10.37')
	cursor = db.cursor()
	rightsql = 'SELECT count(id) FROM case_apitest WHERE apitestresult=TRUE'
	rightresult = cursor.execute(rightsql)
	apis_pass_count = [row[0] for row in cursor.fetchmany(rightresult)][0]
	worngsql = 'SELECT count(id) FROM case_apitest WHERE apitestresult=FALSE'
	wrongresult = cursor.execute(worngsql)
	apis_fail_count = [row[0] for row in cursor.fetchmany(wrongresult)][0]
	db.close()
	return render(request, "task_scence_report.html",
				  {"user": username, "apis": apis_list, "apiscounts": apis_count, "apis_pass_counts": apis_pass_count,
				   "apis_fail_counts": apis_fail_count})  # 把值赋给apiscounts 变量


def login(request):
	if request.session.get('is_login', None):
		return redirect('login.html')

	if request.POST:
		username = password = ''
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(username=username, password=password)
		if user is not None and user.is_active:
			auth.login(request, user)
			request.session["login_user"] = username
			# 跳转主页
			response = HttpResponseRedirect('/home/')
			return response
		else:
			message = "账号或密码不正确，请重新输入"
	# return render(request, 'login.html', {'error': 'username or password error'})
	return render(request, 'login.html', locals())


@login_required
def home(request):
	username = request.session.get('user', '')
	if username is None:
		return HttpResponseRedirect('/login/')
	else:
		return HttpResponseRedirect( '/api/')


def logout(request):
	request.session.flush()
	return render(request, 'login.html', locals())


@login_required
def api_test_report(request):
	username = request.session.get('user', '')
	apis_list = SingeApi.objects.all()
	apis_count = SingeApi.objects.all().count()  # 统计接口数
	db = pymysql.connect(user='root', db='web', passwd='root', host='127.0.0.1')
	cursor = db.cursor()
	rightsql = 'SELECT count(id) FROM case_singeapi WHERE apistatus=TRUE'
	rightresult = cursor.execute(rightsql)
	apis_pass_count = [row[0] for row in cursor.fetchmany(rightresult)][0]
	worngsql = 'SELECT count(id) FROM case_singeapi WHERE apistatus=FALSE'
	wrongresult = cursor.execute(worngsql)
	apis_fail_count = [row[0] for row in cursor.fetchmany(wrongresult)][0]
	db.close()
	return render(request, "task_api_report.html",
				  {"user": username, "apiss": apis_list, "apiscounts": apis_count, "apis_pass_counts": apis_pass_count,
				   "apis_fail_counts": apis_fail_count})  # 把值赋给apiscounts 变量


# 定时任务
@login_required
def periodic_task(request):
	username = request.session.get('user', '')
	task_list = PeriodicTask.objects.all()
	task_count = PeriodicTask.objects.all().count()  # 统计数
	periodic_list = IntervalSchedule.objects.all()  # 周期任务 （如：每隔1小时执行1次）
	crontab_list = CrontabSchedule.objects.all()  # 定时任务 （如：某年月日的某时，每天的某时）
	paginator = Paginator(task_list, 10)  # 生成paginator对象,设置每页显示10条记录
	page = request.GET.get('page', 1)  # 获取当前的页码数,默认为第1页
	currentPage = int(page)  # 把获取的当前页码数转换成整数类型
	try:
		task_list = paginator.page(page)  # 获取当前页码数的记录列表
	except PageNotAnInteger:
		task_list = paginator.page(1)  # 如果输入的页数不是整数则显示第1页的内容
	except EmptyPage:
		task_list = paginator.page(paginator.num_pages)  # 如果输入的页数不在系统的页数中则显示最后一页的内容
	return render(request, "periodic_task.html", {"user": username, "tasks": task_list, "taskcounts": task_count,
												  "periodics": periodic_list, "crontabs": crontab_list})


@login_required
# 运行单接口测试
def do_single(request):
	username = request.session.get('user', '')
	caseId = apitestId = request.GET.get('api.id', None)
	single_api_test(caseId)
	api = SingeApi.objects.get(id=caseId)
	return render(request, 'api_result.html', {'username': username, "api": api})


# 搜索功能
@login_required
def search(request):
	username = request.session.get('user', '')  # 读取浏览器登录session
	searchTxT = request.GET.get("search", "")
	datalist = do_search(searchTxT)
	total = len(datalist)
	return render(request, 'search_result.html', {"user": username, "datas": datalist, 'total': total})

@login_required
# 运行单场景接口测试
def do_apitest(request):
	username = request.session.get('user', '')
	apitestId = request.GET.get('apitest.id', None)
	api = Apitest.objects.get(id=apitestId)  # 获取所有接口测试用例
	steps = Apistep.objects.all()
	single_scence_test(apitestId)
	return render(request, 'apitest_result.html', {'username': username, "api": api, 'steps': steps})

# 关闭bug
@login_required
def colse_bug(request):
	username = request.session.get('user', '')
	bugId = request.GET.get('bug.id', None)
	close_bug(bugId)
	return HttpResponse('关闭当前bug')