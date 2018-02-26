#!/bin/bash

host="localhost:9200"
headers="Content-Type: application/json"

services=(
    "music|dicCommon"
    "story|dicCommon"
    "poetry|dicCommon"
)

for index in ${services[@]}; do
    arg=${index%%|*}
    curl -XDELETE "${host}/${arg}"
done

#curl -XDELETE "${host}/yyd"

python init_service.py init

curl -XPOST "${host}/_all/_close"
for service in ${services[@]}; do
    args=($(echo ${service} | tr '|' ' '))
    curl -H "${headers}" -XPUT "${host}/${args[0]}/_settings" -d "{
      \"similarity\": {
        \"yyd_bm25\": {
          \"type\": \"BM25\",
          \"b\": 0
        }
      },
      \"analysis\": {
        \"tokenizer\": {
          \"${args[0]}_ansj\": {
            \"type\": \"dic_ansj\",
            \"dic\": \"${args[1]}\",
            \"stop\": \"stop\",
            \"ambiguity\": \"ambiguity\",
            \"synonyms\": \"synonyms\",
            \"crf\": \"crf\",
            \"isNameRecognition\": \"true\",
            \"isNumRecognition\": \"true\",
            \"isQuantifierRecognition\": \"true\",
            \"isRealName\": \"false\",
            \"isSkipUserDefine\": \"false\"
          }
        },
        \"analyzer\": {
          \"${args[0]}_ansj\": {
            \"type\": \"custom\",
            \"tokenizer\": \"${args[0]}_ansj\"
          }
        }
      }
    }"
done
curl -XPOST "${host}/_all/_open"

#sleep 0.2

for item in ${services[@]}; do
    arg=${item%%|*}
    curl -H "${headers}" -XPOST "${host}/${arg}/default/_mapping" -d "{
        \"default\": {
            \"properties\": {
                \"template\":{
                    \"analyzer\": \"${arg}_ansj\",
                    \"type\": \"text\",
                    \"similarity\": \"yyd_bm25\"
                }
            }
        }
    }"
done

echo

python init_service.py dic

