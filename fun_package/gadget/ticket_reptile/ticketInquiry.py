# coding=gbk
import requests
import re
import urllib3
from pprint import pformat
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9098'

# url����

request_value = requests.get(url, verify=False)
# ��ȡ��ҳ��Ϣ�����ж�֤��
pattern = u'([\u4e00-\u9fa5]+)\\|([A-Z]+)'
# ������ʽ��ȡ�����Լ���дӢ����ĸ
result = re.findall(pattern, request_value.text)
# ��ȡ������Ϣ
station = pformat(dict(result), indent=4)
# ������ȡ����Ϣת���ֵ�һһ��Ӧ����վ��
# д���ļ���
f = open("station.py", "w", encoding='utf-8')
f.write(station)
f.close()
