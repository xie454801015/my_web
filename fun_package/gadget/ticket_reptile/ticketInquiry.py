# coding=gbk
import requests
import re
import urllib3
from pprint import pformat
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9098'

# url变量

request_value = requests.get(url, verify=False)
# 提取网页信息，不判断证书
pattern = u'([\u4e00-\u9fa5]+)\\|([A-Z]+)'
# 正则表达式提取中文以及大写英文字母
result = re.findall(pattern, request_value.text)
# 提取所需信息
station = pformat(dict(result), indent=4)
# 把所获取的信息转成字典一一对应（车站）
# 写入文件中
f = open("station.py", "w", encoding='utf-8')
f.write(station)
f.close()
