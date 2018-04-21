# encoding: utf-8
"""拷贝藏宝阁的所有js文件"""
import sys
import requests
import re
url = sys.argv[1]
# url = """http://xyq.cbg.163.com/cgi-bin/equipquery.py?act=show_overall_search_pet"""
import os
cbg_backup_file = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0,  cbg_backup_file)

r = requests.get(url)
res = re.findall('<script\s+.*?src="(.*?\.js)">', r.text)
for js in res:
    r = requests.get(js)
    path = js.split('.com/')[1]
	
    p = os.path.join(cbg_backup_file, 'static', path)
    print(p)
    if not os.path.exists(os.path.dirname(p)):
        os.makedirs(os.path.dirname(p))
    with open(p, 'wb') as f:
        f.write(r.content)




