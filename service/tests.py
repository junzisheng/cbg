import requests
import json
a = [1,2]

requests.post('http://127.0.0.1:8000/api/proxy_delete', data={'id_list': [7,8]})