#-*- coding:utf-8 -*-

import requests

service = "song"

resp = requests.get("http://127.0.0.1:9200/" + service + "/_analyze", json = {
    "analyzer" : service + "_ansj",
    "text" : "我想听歌",
})

rs = resp.json()
print rs

for i in rs["tokens"]:
    print i["token"], i["type"]
