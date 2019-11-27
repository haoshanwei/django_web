from __future__ import absolute_import

# !user/bin/python
# -*- coding: utf-8 -*-
__author__: 'huangsonglin@dcpai.cn'
__Time__: '2019/9/29 17:46'

import os
import pymysql
import requests, time, sys
import json
import random, re
import hashlib
import datetime, time
from apitest.mysql import Mysql, TestMysql

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))

host = Mysql().reslut_replace(f'select value from parameter_parameter where name="host"')
web_host = Mysql().reslut_replace(f'select value from parameter_parameter where name="web_host_1"')
headers = Mysql().reslut_replace('select value from parameter_parameter where name="headers"')
user = Mysql().reslut_replace('select value from parameter_parameter where name="web_admin"')
password = Mysql().reslut_replace('select value from parameter_parameter where name="web_admin_password"')
web_headers = {'Content-Type': 'application/x-www-form-urlencoded',
           'Referer': f'{web_host}/admin/login',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                         '(KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36'}


def _get_csrf():
	url = f'{web_host}/admin/login'
	r = requests.get(url)
	R = re.compile('<input type="hidden" name=".*" value="(.*?)" />')
	csrf = re.findall(R, r.text)
	return csrf


# 登录
def login(func):
	def wrapper():
		s = requests.session()
		url = f'{web_host}/admin/login'
		_csrf = _get_csrf()
		data = {'username': user, 'password': password, '_csrf': _csrf}
		r = s.post(url, data=data, headers=web_headers)
		Cookie = (s.cookies.get_dict())
		Cookie = list(Cookie.keys())[0] + '=' + list(Cookie.values())[0]
		R = re.compile('request.setRequestHeader.*, "(.*?)"')
		X_CSRF_TOKEN = re.findall(R, r.text)[0]
		web_headers.update(Cookie=Cookie)
		web_headers.update({"X-CSRF-TOKEN": X_CSRF_TOKEN})
		func()
	return wrapper

@login
def add_bid_product():
	url = web_host + '/admin/product/productAdd'
	data = {'id': '',  # 商品ID
			'version': '',  #
			'name': time.asctime(),  # 商品名字
			'type': f"P_T_0{random.randint(1,5)}",  # 商品类型
			# 预计拍卖时长
			'planTime': 'P_P_02',
			'marketPrice': f'P_M_0{random.randint(1,6)}',  # 市场预估价
			'beginPrice': random.randint(0, 100),  # 起拍价
			'bidInc': 'B_I_03',  # 加价幅度
			'desc': f'拍品创建于:{time.asctime()}.',
			'images': Mysql().reslut_replace(f'select url from img order by rand() limit 1'),  # 封面图片
			'file': '',  #
			'lot3dFilePath': '',  # 3D图
			'attachments': Mysql().reslut_replace(f'select url from img order by rand() limit 1'),  # 简介图
			'video': '',  # 视频
			'videoImage': '',  # 视频文件图片
			# 字体详情定义样式
			'markFonts': ''}
	req = requests.post(url, data=data, headers=web_headers, timeout=2)
	return req

@login
def add_delay_product():
		url = web_host + '/admin/product/delayProductAdd'
		data = {'id': '',
				'version': '',
				'name': time.asctime(),
				'type': f"P_T_0{random.randint(1,3)}",
				'marketPriceValue': random.randint(5000, 1000000),
				'beginPrice': random.randint(0, 100),
				'bidIncValue': random.randrange(100, 500, 100),
				'desc': f'拍品创建于:{time.asctime()}.',
				'images': Mysql().reslut_replace(f'select url from img order by rand() limit 1'),
				'video': '', 'videoImage': '', 'noSiteMeshWapper': 'true'}
		req = requests.post(url, data=data, headers=web_headers, timeout=2)
		return req


@login
def add_bid_live_auction():
	url = web_host + '/admin/auction/auctionAdd'
	can_use_url = web_host + '/admin/product/findCanAuctionProductPage'
	update_url = web_host + '/admin/lot/updateLotDeliverPeople'
	pass_url = web_host + '/admin/auction/auctionApprPass'
	can_data = {'page': 1, "rows": 20}
	can_use_req = requests.get(can_use_url, headers=web_headers, params=can_data)
	can_user_product = can_use_req.json()
	productIdList = ''
	if int(can_user_product['total']) <= 5:
		for i in range(5):
			add_bid_product()
		can_use_req = requests.get(can_use_url, headers=web_headers, params=can_data)
		can_user_product = can_use_req.json()
	for result in can_user_product['rows']:
		if can_user_product['rows'].index(result) <= 10:
			productIdList += '%s,' % str(result['id'])
		else:
			break
	productIdList = productIdList.strip(',')
	data = {'id': '',  # 拍场ID
			'version': '',  # 版本号
			'name': time.asctime(),  # 拍场名称
			'startTime': (datetime.datetime.now() + datetime.timedelta(minutes=5)).strftime('%Y-%m-%d %H:%M:%S'),
			# 拍场开始时间
			'keyword': time.asctime(),  # 拍场关键字
			'auctionType': "A_T_03",  # 拍场类型
			'preEnter': "A_P_09",  # 提前入场类型
			'perActionDelay': "A_D_01",  # 每次出价延时
			'celebrateDuration': "A_PT_01",  # 庆祝时间
			'warmDuration': "A_I_01",  # 预热时长
			'countDownTime': "C_D_T_01",  # 出价倒计时
			"liveSuperAnchor": 1,  # 是否超级主播。如果为False时，auctioneerId就为空默认商家
			# 拍卖师--写死，对应账号：19900000008
			'auctioneerId': "AUC_4",
			# 主播账号，写死：19900000009
			'liveAuctioneerId': "L_AUC_4",
			'useGroup': 1,
			'desc': f'拍场创建于:{time.asctime()}.',
			'icon': Mysql().reslut_replace(f'select url from img order by rand() limit 1'),  # 拍场图片地址
			'productIdList': productIdList,
			'noSiteMeshWapper': 'true'}
	req = requests.post(url, data=data, headers=web_headers)
	auctionId = TestMysql().reslut_replace\
		(f'SELECT id FROM auction WHERE member_id=5152 AND appr_state="W" ORDER BY create_time DESC')
	lot_list = TestMysql().reslut_replace(f'SELECT GROUP_CONCAT(id) FROM lot WHERE auction_id={auctionId} GROUP BY auction_id')
	lot_list = lot_list.split(',')
	for lotId in lot_list:
		data = {'lotId': lotId, 'deliverPeople': "NULL"}
		requests.get(update_url, params=data, headers=web_headers)
	update_data = {'_method': 'put', 'auctionId': auctionId}
	requests.post(pass_url, data=update_data, headers=web_headers)


# 创建图文拍场
@login
def add_bid_image_text_auction():
	url = web_host + '/admin/auction/auctionAdd'
	can_use_url = web_host + '/admin/product/findCanAuctionProductPage'
	update_url = web_host + '/admin/lot/updateLotDeliverPeople'
	pass_url = web_host + '/admin/auction/auctionApprPass'
	can_data = {'page': 1, "rows": 20}
	can_use_req = requests.get(can_use_url, headers=web_headers, params=can_data)
	can_user_product = can_use_req.json()
	productIdList = ''
	if int(can_user_product['total']) <= 5:
		for i in range(5):
			add_bid_product()
		can_use_req = requests.get(can_use_url, headers=web_headers, params=can_data)
		can_user_product = can_use_req.json()
	for result in can_user_product['rows']:
		if can_user_product['rows'].index(result) <= 10:
			productIdList += '%s,' % str(result['id'])
		else:
			break
	productIdList = productIdList.strip(',')
	data = {'id': '',  # 拍场ID
			'version': '',  # 版本号
			'name': time.asctime(),  # 拍场名称
			'startTime': (datetime.datetime.now() + datetime.timedelta(minutes=2)).strftime('%Y-%m-%d %H:%M:%S'),
			# 拍场开始时间
			'keyword': time.asctime(),  # 拍场关键字
			'auctionType': "A_T_03",  # 拍场类型
			'preEnter': "A_P_09",  # 提前入场类型
			'perActionDelay': "A_D_01",  # 每次出价延时
			'celebrateDuration': "A_PT_01",  # 庆祝时间
			'warmDuration': "A_I_01",  # 预热时长
			'countDownTime': "C_D_T_01",  # 出价倒计时
			"liveSuperAnchor": None,
			'auctioneerId': "AUC_4",
			'liveAuctioneerId': None,
			'useGroup': 1,
			'desc': f'拍场创建于:{time.asctime()}.',
			'icon': Mysql().reslut_replace(f'select url from img order by rand() limit 1'),  # 拍场图片地址
			'productIdList': productIdList,
			'noSiteMeshWapper': 'true'}
	req = requests.post(url, data=data, headers=web_headers)
	auctionId = TestMysql().reslut_replace \
		(f'SELECT id FROM auction WHERE member_id=5152 AND appr_state="W" ORDER BY create_time DESC')
	lot_list = TestMysql().reslut_replace(
		f'SELECT GROUP_CONCAT(id) FROM lot WHERE auction_id={auctionId} GROUP BY auction_id')
	lot_list = lot_list.split(',')
	for lotId in lot_list:
		data = {'lotId': lotId, 'deliverPeople': "NULL"}
		requests.get(update_url, params=data, headers=web_headers)
	update_data = {'_method': 'put', 'auctionId': auctionId}
	requests.post(pass_url, data=update_data, headers=web_headers)


# 创建商家直播的拍场
@login
def add_sellself_live_bid_auction():
	url = web_host + '/admin/auction/auctionAdd'
	can_use_url = web_host + '/admin/product/findCanAuctionProductPage'
	update_url = web_host + '/admin/lot/updateLotDeliverPeople'
	pass_url = web_host + '/admin/auction/auctionApprPass'
	can_data = {'page': 1, "rows": 20}
	can_use_req = requests.get(can_use_url, headers=web_headers, params=can_data)
	can_user_product = can_use_req.json()
	productIdList = ''
	if int(can_user_product['total']) <= 5:
		for i in range(5):
			add_bid_product()
		can_use_req = requests.get(can_use_url, headers=web_headers, params=can_data)
		can_user_product = can_use_req.json()
	for result in can_user_product['rows']:
		if can_user_product['rows'].index(result) <= 10:
			productIdList += '%s,' % str(result['id'])
		else:
			break
	productIdList = productIdList.strip(',')
	data = {'id': '',  # 拍场ID
			'version': '',  # 版本号
			'name': time.asctime(),  # 拍场名称
			'startTime': (datetime.datetime.now() + datetime.timedelta(minutes=5)).strftime('%Y-%m-%d %H:%M:%S'),
			# 拍场开始时间
			'keyword': time.asctime(),  # 拍场关键字
			'auctionType': "A_T_03",  # 拍场类型
			'preEnter': "A_P_09",  # 提前入场类型
			'perActionDelay': "A_D_01",  # 每次出价延时
			'celebrateDuration': "A_PT_01",  # 庆祝时间
			'warmDuration': "A_I_01",  # 预热时长
			'countDownTime': "C_D_T_01",  # 出价倒计时
			"liveSuperAnchor": 0,  # 是否超级主播。如果为False时，auctioneerId就为空默认商家
			# 拍卖师--写死，对应账号：19900000008
			'auctioneerId': "AUC_4",
			# 主播账号，写死：19900000009
			'liveAuctioneerId': "",
			'useGroup': 1,
			'desc': f'拍场创建于:{time.asctime()}.',
			'icon': Mysql().reslut_replace(f'select url from img order by rand() limit 1'),  # 拍场图片地址
			'productIdList': productIdList,
			'noSiteMeshWapper': 'true'}
	req = requests.post(url, data=data, headers=web_headers)
	auctionId = TestMysql().reslut_replace \
		(f'SELECT id FROM auction WHERE member_id=5152 AND appr_state="W" ORDER BY create_time DESC')
	lot_list = TestMysql().reslut_replace(
		f'SELECT GROUP_CONCAT(id) FROM lot WHERE auction_id={auctionId} GROUP BY auction_id')
	lot_list = lot_list.split(',')
	for lotId in lot_list:
		data = {'lotId': lotId, 'deliverPeople': "NULL"}
		requests.get(update_url, params=data, headers=web_headers)
	update_data = {'_method': 'put', 'auctionId': auctionId}
	requests.post(pass_url, data=update_data, headers=web_headers)

# 添加秒啪拍场
@login
def add_delay_auction():
	expectedStartTime = (datetime.datetime.now() + datetime.timedelta(minutes=3))
	expectedEndTime = (expectedStartTime + datetime.timedelta(minutes=50))
	productIdList = TestMysql().reslut_replace \
		(f'SELECT SUBSTRING_INDEX(GROUP_CONCAT(id ORDER BY id DESC),",", 10) from product WHERE member_id=5152 '
		 f'AND valid=TRUE AND bid_model="AUC_DELAY" AND sold_out=FALSE AND source="APP" AND in_auction=FALSE '
		 f'GROUP BY member_id')
	if len(productIdList.split(',')) == 0:
		for i in range(10):
			self.delayProductAdd()
		productIdList = TestMysql().reslut_replace \
			(f'SELECT SUBSTRING_INDEX(GROUP_CONCAT(id ORDER BY id DESC),",", 10) from product WHERE member_id=5152 '
			 f'AND valid=TRUE AND bid_model="AUC_DELAY" AND sold_out=FALSE AND source="APP" AND in_auction=FALSE '
			 f'GROUP BY member_id')
	url = web_host + '/admin/auction/delayAuctionAdd'
	data = {"id": '', "version": "", "categoryCode": "A_D_T_01", "buyerCommissionPercent": '0',
			"name": time.asctime(), "bidBondAmount": random.randrange(0, 5000, 1000), "freePost": 1,
			"guaranteeCommission": '', "scheduled": True,
			'icon': Mysql().reslut_replace(f'select url from img order by rand() limit 1'),
			"expectedStartTime": expectedStartTime.strftime("%Y-%m-%d %H:%M:%S"), "desc": (time.asctime() + '\n') * 20,
			"expectedEndTime": expectedEndTime.strftime("%Y-%m-%d %H:%M:%S"),
			"productIdList": productIdList, "noSiteMeshWapper": True}
	requests.post(url, data=data, headers=web_headers)
	auctionId = TestMysql().reslut_replace\
		(f'select id from auction where member_id=5152 AND bid_model="AUC_DELAY" AND valid=TRUE AND source="APP" '
		 f'AND appr_state="D" and auction_state="N" order by id desc')
	push_url = web_host + '/admin/auction/publishAuction'
	push_data = {"auctionId": auctionId, "_method": "put"}
	requests.post(push_url, data=push_data, headers=web_headers)

# 注册
def register(user, pwd, name):
	url = host + 'interface/mobile/pmall/registerByPhone_220'
	code_url = host + 'interface/mobile/pmall/sendAuthenticationCode_112'
	requests.post(code_url, data={"phoneNum": int(user)}, headers=headers)
	time.sleep(1)
	code = TestMysql().reslut_replace(f'SELECT message from sms_send_his WHERE phone={user}')
	code = re.findall('是(.*)，5', code)[0]
	md = hashlib.md5()
	md.update(str(pwd).encode(encoding='utf-8'))
	pwd = md.hexdigest()
	data = {'countryCode': '86', 'code': code, 'nickname': name, 'phoneNum': user, 'pwd': pwd}
	req = requests.post(url, data=data, headers=headers)
	return req


if __name__ == '__main__':
	register(1,1)