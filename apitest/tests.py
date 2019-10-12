from django.test import TestCase

# Create your tests here.
result = """
{"beginPrice":"0","bidInc":"B_I_11","desc":"尺寸长180mm直径45mm佛家至宝元代天铁+紫利玛铜+黄利玛铜三色九股金刚杵","images":"2D7DF2D1-303F-4504-A37C-F9F92C9A97270.JPG","marketPrice":"P
_M_06","name":"斯瓦{"beginPrice":"0","bidInc":"B_I_11","desc":"尺寸长180mm直径45mm佛家至宝元代天铁+紫利玛铜+黄利玛铜三色九股金刚杵","images":"2D7DF2D1-303F-4504-A37C-F9F92C9A97270.JP
G","marketPrice":"P_M_06","name":"斯瓦特","planTime":"P_P_01","type":"P_T_01"}


	"""

result.replace('"',"'")
import json

print(eval(result))