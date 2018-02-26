#!/bin/bash

host=127.0.0.1
user=root
passwd=123456
dbname=yyd_resources

dirname=/home/es/packages/elasticsearch-6.1.1/config/yyd-semantic-es/dic

CMD="mysql -h${host} -u${user} -p${passwd} ${dbname}"

echo "SELECT name, 'c:song', 1 FROM tb_music_resource;" | exec ${CMD} > ${dirname}/song.dic
echo "SELECT name, 'c:songer', 1 FROM tb_music_singer;" | exec ${CMD} > ${dirname}/songer.dic
echo "SELECT name, 'c:storyName', 1 FROM tb_story_resource;" | exec ${CMD} > ${dirname}/storyName.dic
echo "SELECT title, 'c:poetryTitle', 1 FROM tb_poetry;" | exec ${CMD} > ${dirname}/poetryTitle.dic
echo "SELECT sentence, 'c:poetrySentence', 1 FROM tb_sentence;" | exec ${CMD} > ${dirname}/poetrySentence.dic

sed -i '1d' ${dirname}/song.dic
sed -i '1d' ${dirname}/songer.dic
sed -i '1d' ${dirname}/storyName.dic
sed -i '1d' ${dirname}/poetryTitle.dic
sed -i '1d' ${dirname}/poetrySentence.dic
