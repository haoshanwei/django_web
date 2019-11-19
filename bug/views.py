from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from bug.models import Bug
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.

@login_required
def bug(request):
	username = request.session.get('user', '')
	buglist = Bug.objects.all()
	bug_count = Bug.objects.all().count()
	paginator = Paginator(buglist, 10)  # 生成paginator对象,设置每页显示10条记录
	page = request.GET.get('page', 1)  # 获取当前的页码数,默认为第1页
	currentPage = int(page)  # 把获取的当前页码数转换成整数类型
	try:
		buglist = paginator.page(page)  # 获取当前页码数的记录列表
	except PageNotAnInteger:
		buglist = paginator.page(1)  # 如果输入的页数不是整数则显示第1页的内容
	except EmptyPage:
		buglist = paginator.page(paginator.num_pages)  # 如果输入的页数不在系统的页数中则显示最后一页的内容
	return render(request, 'bug.html', {'user': username, 'bugs': buglist})





