#!/bin/bash

host=127.0.0.1
user=root
passwd=123456
dbname=yyd_resources

CMD="mysql -h${host} -u${user} -p${passwd} ${dbname}"

echo "SELECT name, 'c:song', 1 FROM tb_music_resource;" | exec ${CMD} > ../dic/song.dic
echo "SELECT name, 'c:songer', 1 FROM tb_music_singer;" | exec ${CMD} > ../dic/songer.dic
echo "SELECT name, 'c:storyName', 1 FROM tb_story_resource;" | exec ${CMD} > ../dic/storyName.dic
echo "SELECT title, 'c:poetryTitle', 1 FROM tb_poetry;" | exec ${CMD} > ../dic/poetryTitle.dic
echo "SELECT sentence, 'c:poetrySentence', 1 FROM tb_sentence;" | exec ${CMD} > ../dic/poetrySentence.dic

sed -i '1d' ../dic/song.dic
sed -i '1d' ../dic/songer.dic
sed -i '1d' ../dic/storyName.dic
sed -i '1d' ../dic/poetryTitle.dic
sed -i '1d' ../dic/poetrySentence.dic
