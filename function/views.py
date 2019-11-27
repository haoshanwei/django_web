from django.shortcuts import render
from function.models import Function
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .tasks import *
from apitest.mysql import TestMysql
from django.http import JsonResponse
from django.contrib import messages
from django.http.response import HttpResponse
# Create your views here.

@login_required
def Add_Bid_product(request):
	username = request.session.get('user', '')
	add_bid_product()
	return HttpResponse('恭喜,轰啪拍品创建成功')

@login_required
def Add_Delay_product(request):
	username = request.session.get('user', '')
	add_delay_product()
	return HttpResponse('恭喜,秒啪拍品创建成功')

@login_required
def Add_Delay_Auction(request):
	username = request.session.get('user', '')
	add_delay_auction()
	return HttpResponse('恭喜,秒啪拍场创建成功')

@login_required
def Add_Bid_Live_Auction(request):
	username = request.session.get('user', '')
	add_bid_live_auction()
	return HttpResponse('恭喜,创建轰啪直播拍场成功')

@login_required
def Add_Bid_ImageText_Auction(request):
	username = request.session.get('user', '')
	add_bid_image_text_auction()
	return HttpResponse('恭喜,创建轰啪图文拍场成功')

@login_required
def Add_Seller_Live_Auction(request):
	username = request.session.get('user', '')
	add_sellself_live_bid_auction()
	return HttpResponse('恭喜,创建商家直播拍场成功')

@login_required
def function(request):
	username = request.session.get('user', '')
	func_list = Function.objects.all()
	return render(request, 'function.html', {"user": username, 'functions': func_list})


