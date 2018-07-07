import requests
import datetime
import sys

import time
import json

if __name__ == '__main__':
    url = """
    http://xyq-android2.cbg.163.com/app2-cgi-bin/app_search.py?act=super_query&search_type=overall_pet_search&order_by=selling_time+DESC&is_baobao=1
    """
    while True:
        try:
            r = requests.get(url)
            print(r.text)
            sys.stdout(r.status_code)
            if json.loads(r.text)['status'] != 1:
                sys.stdout(datetime.datetime.now())
                break
        except:
            pass
        time.sleep(2)