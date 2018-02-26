#-*- coding:utf-8 -*-

import requests

resp = requests.get("http://127.0.0.1:9200/_analyze", json = {
    "analyzer" : "dic_ansj",
    "text" : "我想听我的一天",
})

rs = resp.json()
print rs

for i in rs["tokens"]:
    print i["token"], i["type"]
