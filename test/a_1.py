# url = """http://recommd.xyq-android2.cbg.163.com/cgi-bin/recommend.py?act=recommd_by_role&count=150&search_type=overall_pet_search&order_by=selling_time+DESC&'"""
import requests
import json
# r = requests.get(url)
# = json.loads(r.text)
# l = r['equips']
# print(len(l))
import json
import time
now = time.time()
# url = 'http://47.104.193.247/index?timestamp=%s' % now
# url = 'http://shadow.namibox.com/'
# url = 'http://121.199.79.144:80'
# url = 'http://120.26.215.192?m=222' # 外研社
# url = 'http://47.98.229.132/service/index'  # 2
url = 'https://namibox.com/123123'
r = requests.get(url)
print(r.text, time.time() - now)


