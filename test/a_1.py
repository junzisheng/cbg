url = """http://recommd.xyq-android2.cbg.163.com/cgi-bin/recommend.py?act=recommd_by_role&count=150&search_type=overall_pet_search&order_by=selling_time+DESC&'"""
import requests
import json
r = requests.get(url)
r = json.loads(r.text)
l = r['equips']
print(len(l))
import json


