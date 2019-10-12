#!user/bin/python
# -*- coding: utf-8 -*-
__author__: 'huangsonglin@dcpai.cn'
__Time__: '2019/9/29 17:55'

import os
import sys
import pymysql

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
"""
@author: 黄松林
@create time: Aug.1 2018
@description: 该类主要功能是链接数据库然后执行查询，反馈想要的结果
"""


class Mysql:

	# 进入数据库
	def into_mysql(self):
		db = pymysql.connect(user='root', db='web', passwd='root', host='127.0.0.1')
		# 建立游标池
		db = db.cursor()
		return db

	# 执行查询
	def sql_result(self, sql):
		db = self.into_mysql()
		try:
			db.execute(sql)
			data = db.fetchall()
			return list(data)
		except():
			raise ValueError('查询出错')

	# 更新语句
	def updata(self, sql):
		db = self.into_mysql()
		db.execute(sql)
		db.connection.commit()

	# 删除语句
	def delete(self, sql):
		db = self.into_mysql()
		db.execute(sql)
		db.connection.commit()

	# 查询结果转换
	def reslut_replace(self, sql):
		result = self.sql_result(sql)
		if result == []:
			result = ''
		else:
			result = result[0][0]
		return str(result)

	# 执行其他操作
	def user_database(self, sql):
		db = self.into_mysql()
		db.execute(sql)

if __name__ == '__main__':
	sql = f'SELECT id, apiname, apiurl, apimethod, apiparamvalue, apiheaders, apiresult, apistatuscode, `apistatus` ' \
		  f'from case_apistep where Apitest_id=2 order by id'
	apis = Mysql().sql_result(sql)
	print(apis)