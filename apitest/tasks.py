from __future__ import absolute_import
#!user/bin/python
# -*- coding: utf-8 -*-
__author__: 'huangsonglin@dcpai.cn'
__Time__: '2019/9/29 17:46'

import os
import pymysql
import requests, time, sys
import json
from web_test.celery import app
from apitest.mysql import Mysql
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))


@app.task
def hello_world():
	print('已运行')


@app.task
# 所有的单一接口测试
def api_test():
	sql = "SELECT id, `apiname`, apiurl, apimethod, apiparamvalue, apiresult, `apistatus`, apistatuscode," \
		  "  ItemsApplication_id, apiheaders from case_singeapi "
	caselist = Mysql().sql_result(sql)
	case_list = []
	for ii in caselist:
		case_list.append(ii)
	Doapi(case_list)


def Doapi(case_list):
	res_flags = []
	request_urls = []
	responses = []
	try:
		host = 'select value from parameter_parameter where name="host"'
		defult_headers = 'select value from parameter_parameter where name="headers"'
		host = Mysql().reslut_replace(host)
		defult_headers = Mysql().reslut_replace(defult_headers)
	except:
		host = None
		defult_headers = None
	for case in case_list:
		try:
			case_id = case[0]
			case_name = case[1]
			case_url = host + case[2]
			case_method = case[3]
			case_param = case[4]
			try:
				if case_param is None or case_param == '/':
					case_param = None
				else:
					case_param = json.loads(case_param.replace("'", '"'))
			except:
				case_param = None
			res_check = case[5]
			case_code = case[7]
			case_headers = case[-1]
			ItemAppId = case[-2]
			try:
				if case_headers is None or case_headers == '/':
					case_headers = defult_headers
					case_headers = json.loads(case_headers.replace("'", '"'))
				else:
					case_headers = json.loads(case_headers.replace("'", '"'))
			except:
				case_headers = eval(defult_headers)
		except Exception as e:
			return '测试用例格式不正确，请严格严重要求添加接口测试案例！ %s' % e
		# get方法
		if case_method.upper() == 'GET':
			req = requests.get(case_url, params=case_param, headers=case_headers)
			responses_code = req.status_code
			responseText = req.text
			if compare_code(responses_code, case_code) and compare_result(responseText) == "PASS":
				res_flags.append('PASS')
				caseWriteResult(case_id, responseText, responses_code, '1')
			else:
				res_flags.append('FAILE')
				caseWriteResult(case_id, responseText, responses_code, '0')
				writeBug(case_id, case_name, case_url, case_param, responses_code, responseText, res_check, ItemAppId)
		if case_method.upper() == 'POST':
			req = requests.post(case_url, data=case_param, headers=case_headers)
			responses_code = req.status_code
			responseText = req.text
			if compare_code(responses_code, case_code) and compare_result(responseText, res_check):
				res_flags.append('PASS')
				caseWriteResult(case_id, responseText, responses_code, '1')
			else:
				res_flags.append('FAILE')
				caseWriteResult(case_id, responseText, responses_code, '0')
				writeBug(case_id, case_name, case_url, case_param, responses_code, responseText, res_check, ItemAppId)
		if case_method.upper() == 'PUT':
			req = requests.put(case_url, data=case_param, headers=case_headers)
			responses_code = req.status_code
			responseText = req.text
			if compare_code(responses_code, case_code) and compare_result(responseText, res_check):
				res_flags.append('PASS')
				caseWriteResult(case_id, responseText, responses_code, '1')
			else:
				res_flags.append('FAILE')
				caseWriteResult(case_id, responseText, responses_code, '0')
				writeBug(case_id, case_name, case_url, case_param, responses_code, responseText, res_check, ItemAppId)
		if case_method.upper() == 'DELETE':
			req = requests.delete(case_url, data=case_param, headers=case_headers)
			responses_code = req.status_code
			responseText = req.text
			if compare_code(responses_code, case_code) and compare_result(responseText, res_check):
				res_flags.append('PASS')
				caseWriteResult(case_id, responseText, responses_code, '1')
			else:
				res_flags.append('FAILE')
				caseWriteResult(case_id, responseText, responses_code, '0')
				writeBug(case_id, case_name, case_url, case_param, responses_code, responseText, res_check, ItemAppId)
		if case_method.upper() == 'PATCH':
			req = requests.patch(case_url, data=case_param, headers=case_headers)
			responses_code = req.status_code
			responseText = req.text
			if compare_code(responses_code, case_code) and compare_result(responseText, res_check):
				res_flags.append('PASS')
				caseWriteResult(case_id, responseText, responses_code, '1')
			else:
				res_flags.append('FAILE')
				caseWriteResult(case_id, responseText, responses_code, '0')
				writeBug(case_id, case_name, case_url, case_param, responses_code, responseText, res_check, ItemAppId)


# 将接口的响应信息写入数据库
def caseWriteResult(case_id, result, code, status):
	now = time.strftime("%Y-%m-%d %H:%M:%S")
	result = result.replace('"',"'")
	sql = f'UPDATE case_singeapi SET case_singeapi.update_time="{now}", ' \
		  f'case_singeapi.apistatuscode="{code}", ' \
		  f'case_singeapi.apiresponse="{result}", ' \
		  f'case_singeapi.apistatus="{status}" ' \
		  f'where case_singeapi.id={case_id}'
	Mysql().updata(sql)

# 编写bug
def writeBug(bug_id, api_name, api_url, request, code, response, res_check, ItemAppId):
	now = time.strftime("%Y-%m-%d %H:%M:%S")
	names = get_bugList_name()
	bugname = str(bug_id) + '_' + api_name + '_出错了'
	bugdetail = '[请求接口]<br />' + api_url + '<br/>' +\
				'[请求数据]<br />' + str(request) + '<br/>' +\
				'[响应状态码]<br />' + str(code) + '<br/>' +\
				'[预期结果]<br/>' + res_check + '<br/>' +\
				'[响应数据]<br />' + str(response) + '<br/>'
	sql = "INSERT INTO bug_bug (bugname, bugdesc, buglevel, bugcreater, createtime, " \
		  "bugstatus, ItemsApplication_id, bugrepair)  " \
		  "VALUES ('%s', '%s', '3', 'admin', '%s', '激活', '%s', 'admin');" % \
		  (bugname, pymysql.escape_string(bugdetail), pymysql.escape_string(now), ItemAppId)
	if api_name in names:
		pass
	else:
		Mysql().updata(sql)

# 预期结果对比
def compare_result(dict_result, result_check):
	"""
	:param result:	接口响应结果
	:param result_check: 预期结果
	:return:
	"""
	if result_check == None or result_check == "/":
		return True
	else:
		dict_result = str(dict_result)[1:-1].replace(':', '=').replace('= ', '=').replace("'",'').replace('"','')
		result_list = str(result_check).split(';')
		for result in result_list:
			if result not in dict_result:
				return False
				break
			else:
				rs.append(True)
		return True

def compare_code(code, check_code):
	if str(code) == str(check_code):
		return True
	else:
		return False



# 单场景测试
def single_scence_test(Apitest_id):
	sql = f'SELECT id, apiname, apiurl, apimethod, apiparamvalue, apiheaders, apiresult, apistatuscode, `apistatus`, Apitest_id ' \
		  f'from case_apistep where Apitest_id={Apitest_id} order by id'
	apis = Mysql().sql_result(sql)
	DoScneceapi(apis)

# 定时任务-场景测试
@app.task
def scence_test():
	sql = f'SELECT id, apiname, apiurl, apimethod, apiparamvalue, apiheaders, apiresult, apistatuscode, `apistatus`, ' \
		  f'Apitest_id from case_apistep'
	results = Mysql().sql_result(sql)
	dict_list = []
	if len(results) > 1:
		for i in range(1, len(results)):
			dict_result = {f'场景{results[i-1][-1]}': [results[i - 1]]}
			if f'场景{results[i-1][-1]}' == f'场景{results[i][-1]}':
				dict_result[f'场景{results[i-1][-1]}'].append(results[i - 1])
			dict_list.append(dict_result)
	else:
		dict_result = {f'场景{results[0][-1]}': [results[0]]}
		dict_list.append(dict_result)
	for api in dict_list:
		apisteps = list(api.values())[0]
		DoScneceapi(apisteps)

# 将结果写入场景测试中
def caseWriteResult_scence(reason, status):
	now = time.strftime("%Y-%m-%d %H:%M:%S")
	reason = pymysql.escape_string(reason).replace('\\n', '&nbsp').replace('"', "'")
	sql = f'UPDATE case_apitest SET case_apitest.update_time="{now}", case_apitest.failreason="{reason}", ' \
		  f'case_apitest.apitestresult={status}'
	Mysql().updata(sql)


# 写入场景测试中的bug
def writeScenceBug(apitest_name, api_name, api_url, request, code, response, res_check):
	now = time.strftime("%Y-%m-%d %H:%M:%S")
	bugname =  '场景测试:  %s_出错了' % apitest_name
	names = get_bugList_name()
	bugdetail = '[场景测试]<br/>' + apitest_name  + '<br/>' +\
				'[错误接口名称]<br/>:' + api_name  + '<br/>'+\
				'[接口地址]<br/>' + api_url + '<br/>' +\
				'[请求数据]<br />' + str(request) + '<br/>' +\
				'[响应状态码]<br />' + str(code) + '<br/>' +\
				'[预期结果]<br/>' + res_check + '<br/>' +\
				'[响应数据]<br />' + str(response) + '<br/>'
	sql = "INSERT INTO bug_bug (bugname, bugdesc, buglevel, bugcreater, createtime, " \
		  "bugstatus, bugrepair)  " \
		  "VALUES ('%s', '%s', '3', 'admin', '%s', '激活', 'admin');" % \
		  (bugname, pymysql.escape_string(bugdetail), pymysql.escape_string(now))
	if bugname in names:
		pass
	else:
		Mysql().updata(sql)


def DoScneceapi(case_list):
	res_flags = []
	request_urls = []
	responses = []
	try:
		host = 'select value from parameter_parameter where name="host"'
		defult_headers = 'select value from parameter_parameter where name="headers"'
		host = Mysql().reslut_replace(host)
		defult_headers = Mysql().reslut_replace(defult_headers)
	except:
		host = None
		defult_headers = None
	for case in case_list:
		try:
			case_id = case[0]
			case_name = case[1]
			case_url = host + case[2]
			case_method = case[3]
			case_param = case[4]
			Apitest_id = case[-1]
			Apitest_name = Mysql().reslut_replace(f'select apitestname from case_apitest where id={Apitest_id}')
			try:
				if case_param is None or case_param == '/':
					case_param = None
				else:
					case_param = json.loads(case_param.replace("'", '"').replace('”', '"'))
			except:
				case_param = None
			res_check = case[6]
			case_code = case[7]
			case_headers = case[5]
			try:
				if case_headers is None or case_headers == '/':
					case_headers = defult_headers
					case_headers = json.loads(case_headers.replace("'", '"'))
				else:
					case_headers = json.loads(case_headers.replace("'", '"'))
			except:
				case_headers = eval(defult_headers)

		except Exception as e:
			return '测试用例格式不正确，请严格严重要求添加接口测试案例！ %s' % e
		# get方法
		if case_method.upper() == 'GET':
			req = requests.get(case_url, params=case_param, headers=case_headers)
			responses_code = req.status_code
			responseText = req.text
			if compare_code(responses_code, case_code) and compare_result(responseText, res_check):
				res_flags.append('PASS')
			else:
				res_flags.append('FAILE')
				reason = f'接口:{case_name}调用出错。\n' \
						 f'错误代码:实际响应code:{responses_code};预期响应code:{case_code}\n' \
						 f'预期结果:{res_check}\n' \
						 f'实际响应结果:{responseText}'
				caseWriteResult_scence(reason, '0')
				writeScenceBug(Apitest_name, case_name, case_url, case_param, responses_code, responseText, res_check)
				break
		if case_method.upper() == 'POST':
			req = requests.post(case_url, data=case_param, headers=case_headers)
			responses_code = req.status_code
			responseText = req.text
			if compare_code(responses_code, case_code) and compare_result(responseText, res_check):
				res_flags.append('PASS')
			else:
				res_flags.append('FAILE')
				reason = f'接口:{case_name}调用出错。\n' \
						 f'错误代码:实际响应code:{responses_code};预期响应code:{case_code}\n' \
						 f'预期结果:{res_check}\n' \
						 f'实际响应结果:{responseText}'
				caseWriteResult_scence(reason, '0')
				writeScenceBug(Apitest_name, case_name, case_url, case_param, responses_code, responseText, res_check)
				break
		if case_method.upper() == 'PUT':
			req = requests.put(case_url, data=case_param, headers=case_headers)
			responses_code = req.status_code
			responseText = req.text
			if compare_code(responses_code, case_code) and compare_result(responseText, res_check):
				res_flags.append('PASS')
			else:
				res_flags.append('FAILE')
				reason = f'接口:{case_name}调用出错。\n' \
						 f'错误代码:实际响应code:{responses_code};预期响应code:{case_code}\n' \
						 f'预期结果:{res_check}\n' \
						 f'实际响应结果:{responseText}'
				caseWriteResult_scence(reason, '0')
				writeScenceBug(Apitest_name, case_name, case_url, case_param, responses_code, responseText, res_check)
				break
		if case_method.upper() == 'DELETE':
			req = requests.delete(case_url, data=case_param, headers=case_headers)
			responses_code = req.status_code
			responseText = req.text
			if compare_code(responses_code, case_code) and compare_result(responseText, res_check):
				res_flags.append('PASS')
			else:
				res_flags.append('FAILE')
				reason = f'接口:{case_name}调用出错。\n' \
						 f'错误代码:实际响应code:{responses_code};预期响应code:{case_code}\n' \
						 f'预期结果:{res_check}\n' \
						 f'实际响应结果:{responseText}'
				caseWriteResult_scence(reason, '0')
				writeScenceBug(Apitest_name, case_name, case_url, case_param, responses_code, responseText, res_check)
				break
		if case_method.upper() == 'PATCH':
			req = requests.patch(case_url, data=case_param, headers=case_headers)
			responses_code = req.status_code
			responseText = req.text
			if compare_code(responses_code, case_code) and compare_result(responseText, res_check):
				res_flags.append('PASS')
			else:
				res_flags.append('FAILE')
				reason = f'接口:{case_name}调用出错。\n' \
						 f'错误代码:实际响应code:{responses_code};预期响应code:{case_code}\n' \
						 f'预期结果:{res_check}\n' \
						 f'实际响应结果:{responseText}'
				caseWriteResult_scence(reason, '0')
				writeScenceBug(Apitest_name, case_name, case_url, case_param, responses_code, responseText, res_check)
				break
		if "FAILE" not in res_flags:
			caseWriteResult_scence("PASS", '1')

def single_api_test(caseId):
	request_urls = []
	responses = []
	try:
		host = 'select value from parameter_parameter where name="host"'
		defult_headers = 'select value from parameter_parameter where name="headers"'
		host = Mysql().reslut_replace(host)
		defult_headers = Mysql().reslut_replace(defult_headers)
	except:
		host =  None
		defult_headers =  None
	sql = f"SELECT id, `apiname`, apiurl, apimethod, apiparamvalue, apiresult, `apistatus`, apistatuscode," \
		  f"  ItemsApplication_id, apiheaders from case_singeapi where id={caseId}"
	case = Mysql().sql_result(sql)[0]
	try:
		case_id = case[0]
		case_name = case[1]
		case_url = host + case[2]
		case_method = case[3]
		case_param = case[4]
		try:
			if case_param is None or case_param == '/':
				case_param = None
			else:
				case_param = json.loads(case_param.replace("'", '"'))
		except:
			case_param = None
		res_check = case[5]
		case_code = case[7]
		case_headers = case[-1]
		ItemAppId = case[-2]
		try:
			if case_headers is None or case_headers == '/':
				case_headers = defult_headers
				case_headers = json.loads(case_headers.replace("'", '"'))
			else:
				case_headers = json.loads(case_headers.replace("'", '"'))
		except:
			case_headers = eval(defult_headers)
	except Exception as e:
		return '测试用例格式不正确，请严格严重要求添加接口测试案例！ %s' % e
	# get方法
	if case_method.upper() == 'GET':
		req = requests.get(case_url, params=case_param, headers=case_headers)
		responses_code = req.status_code
		responseText = req.text
		if compare_code(responses_code, case_code) and compare_result(responseText, res_check):
			caseWriteResult(case_id, responseText, responses_code, '1')
		else:
			caseWriteResult(case_id, responseText, responses_code, '0')
			writeBug(case_id, case_name, case_url, case_param, responses_code, responseText, res_check, ItemAppId)
	if case_method.upper() == 'POST':
		req = requests.post(case_url, data=case_param, headers=case_headers)
		responses_code = req.status_code
		responseText = req.text
		if compare_code(responses_code, case_code) and compare_result(responseText, res_check):
			caseWriteResult(case_id, responseText, responses_code, '1')
		else:
			caseWriteResult(case_id, responseText, responses_code, '0')
			writeBug(case_id, case_name, case_url, case_param, responses_code, responseText, res_check, ItemAppId)
	if case_method.upper() == 'PUT':
		req = requests.put(case_url, data=case_param, headers=case_headers)
		responses_code = req.status_code
		responseText = req.text
		if compare_code(responses_code, case_code) and compare_result(responseText, res_check):
			caseWriteResult(case_id, responseText, responses_code, '1')
		else:
			caseWriteResult(case_id, responseText, responses_code, '0')
			writeBug(case_id, case_name, case_url, case_param, responses_code, responseText, res_check, ItemAppId)
	if case_method.upper() == 'DELETE':
		req = requests.delete(case_url, data=case_param, headers=case_headers)
		responses_code = req.status_code
		responseText = req.text
		if compare_code(responses_code, case_code) and compare_result(responseText, res_check):
			caseWriteResult(case_id, responseText, responses_code, '1')
		else:
			caseWriteResult(case_id, responseText, responses_code, '0')
			writeBug(case_id, case_name, case_url, case_param, responses_code, responseText, res_check, ItemAppId)
	if case_method.upper() == 'PATCH':
		req = requests.patch(case_url, data=case_param, headers=case_headers)
		responses_code = req.status_code
		responseText = req.text
		if compare_code(responses_code, case_code) and compare_result(responseText, res_check):
			caseWriteResult(case_id, responseText, responses_code, '1')
		else:
			caseWriteResult(case_id, responseText, responses_code, '0')
			writeBug(case_id, case_name, case_url, case_param, responses_code, responseText, res_check, ItemAppId)

# 搜索接口
def do_search(searchTxT):
	single_api_sql = f"select apiname, apidesc from case_singeapi where apiname like '%{searchTxT}%'"
	scenect_api_sql = f"select apitestname, apitestdesc from case_apitest where apitestname like '%{searchTxT}%'"
	task_sql = f"select name, task  from djcelery_periodictask where name like '%{searchTxT}%'"
	product_sql = f"select name,`desc` from items_items where name like '%{searchTxT}%'"
	app_sql = f"select name,`desc` from items_itemsapplication where name like '%{searchTxT}%'"
	results = Mysql().sql_result(scenect_api_sql) + Mysql().sql_result(single_api_sql) + Mysql().sql_result(task_sql) +\
			  Mysql().sql_result(product_sql) + Mysql().sql_result(app_sql)
	dict_result = []
	if len(results) == 0:
		pass
	else:
		for result in results:
			new_result = {"name": result[0], "desc": result[1]}
			dict_result.append(new_result)
	return dict_result

# 查看bug名字
def get_bugList_name():
	sql = f"select bugname from bug_bug where bugstatus<>'关闭'"
	nameList = Mysql().sql_result(sql)
	names = []
	for name in nameList:
		names.append(name[0])
	return names

