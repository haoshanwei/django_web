from django.test import TestCase

# Create your tests here.
results = [(1, '登录', 'www.baidu.com', 'get', '1', '/', '/', '200', 1, 1), (2, '登录2', 'www.baidu.com1', 'get', '1', '/', '/', '200', None, 2), (3, '退出', 'www.baidu.com2', 'get', '/', '/', '/', '200', None, 2)]

dict_list = []
for i in range(1, len(results)):
	dict_result = {f'场景{results[i-1][-1]}': [results[i-1][0:-1]]}
	if f'场景{results[i-1][-1]}' == f'场景{results[i][-1]}':
		dict_result[f'场景{results[i-1][-1]}'].append(results[i-1][0:-1])
	dict_list.append(dict_result)


for c in dict_list:
	print(list(c.values())[0])