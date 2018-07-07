import requests
header = {
    'Cookie': 'UM_distinctid=1632e926d6c647-099fb3915846b9-f373567-100200-1632e926d6e6fe; CNZZDATA1260570495=482298516-1525493980-%7C1528524106; sessionid=7ukxo2oiu98ghiocy33zuraeq0dt7pl5; csrftoken=XcY47ChERGJKY7Od9vUz7l7GoKvs0I8d'
}
# url = 'http://127.0.0.1:9000/order/pull_order_data?offset=0&filter={"status": "进行中"}'
# r = requests.get(url, headers=header)
# print(r.text)


url = 'http://127.0.0.1:9000/order/crawl_data_api/?offset=0&filter={"order_id": 9, "old_price__isnull": "True"}'
r = requests.get(url, headers=header)
print(r.text)


