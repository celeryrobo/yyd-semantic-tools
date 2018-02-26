#-*- coding:utf-8 -*-
import sys, re, json, requests

from elasticsearch_dsl import DocType, Text, Q
from elasticsearch_dsl.connections import connections
connections.create_connection(hosts = ["127.0.0.1:9200"])

class Base(DocType):
#    template = Text(analyzer="dic_ansj", search_analyzer="dic_ansj")
    orgTemplate = Text()
    intent = Text()
    params = Text()

class Song(Base):
    class Meta:
        doc_type = "default"
        index = "music"

class Story(Base):
    class Meta:
        doc_type = "default"
        index = "story"

class Poetry(Base):
    class Meta:
        doc_type = "default"
        index = "poetry"

class Intent(object):
    PROG = re.compile("\{(\w+)\}")

    def __init__(self, ident, template, intent, **kw):
        self.ident = ident
        self.template = template
        self.orgTemplate = template
        self.intent = intent
        self.params = self._process(**kw)

    def _process(self, **kw):
        tpl = self.template
        res = self.PROG.findall(tpl)
        for i in res:
            tpl = re.sub(i, kw.get(i, i), tpl)
        self.template = tpl
        return res

    def answer(self, *args):
        return dict(zip(self.params, args))

    def save(self, cls):
        cls(_id = self.ident,
            template = self.template,
            orgTemplate = self.orgTemplate,
            params = ",".join(self.params),
            intent = self.intent).save()

Song.init()
Story.init()
Poetry.init()

#'''
if sys.argv[1] == "dic":
    Song.template = Text(analyzer="song_ansj", search_analyzer="song_ansj")
    Story.template = Text(analyzer="story_ansj", search_analyzer="story_ansj")
    Poetry.template = Text(analyzer="poetry_ansj", search_analyzer="poetry_ansj")
    
    songs = [
    # song
        ((1, "我想听{name}的歌", "bySonger"), {"name":"songer"}),
        ((2, "我想听{name1}的{name2}", "bySongerAndSong"), {"name1":"songer", "name2":"song"}),
        ((3, "我想听歌", "randomPlay"), {}),
        ((4, "我想听{name}", "bySong"), {"name":"song"}),
        ((5, "唱首{name}的歌", "bySonger"), {"name":"songer"}),
        ((6, "我要听{name}", "bySong"), {"name":"song"}),
        ((7, "我想听一首{name}", "bySong"), {"name":"song"}),
        ((8, "我要听一首{name}", "bySong"), {"name":"song"}),
    ]
    stories = [
    # story
        ((11, "说个{name}的故事", "byStoryName"), {"name":"storyName"}),
        ((12, "我想听{name}", "byStoryName"), {"name":"storyName"}),
        ((13, "我想听故事", "randomPlay"), {}),
    ]
    
    poetries = [
    # poetry
        ((21, "是谁写的{sentence}", "autherBySentence"), {"sentence":"poetrySentence"}),
        ((22, "{sentence}是哪首诗中的诗句", "byPoetrySentence"), {"sentence":"poetrySentence"}),
        ((23, "{sentence}的下一句", "nextSentence"), {"sentence":"poetrySentence"}),
        ((24, "{sentence}的上一句", "prevSentence"), {"sentence":"poetrySentence"}),
        ((25, "背一首唐诗{title}", "byPoetryTitle"), {"title":"poetryTitle"}),
        ((26, "背一首{title}", "byPoetryTitle"), {"title":"poetryTitle"}),
        ((27, "背一首唐诗", "randomPlay"), {}),
        ((28, "我想听{title}", "byPoetryTitle"), {"title":"poetryTitle"}),
        ((29, "我想听{sentence}", "byPoetrySentence"), {"sentence":"poetrySentence"}),
    ]
    
    for config, params in songs:
        Intent(*config, **params).save(Song)
    
    for config, params in stories:
        Intent(*config, **params).save(Story)
    
    for config, params in poetries:
        Intent(*config, **params).save(Poetry)
    
    Song._doc_type.refresh()
    Story._doc_type.refresh()
    Poetry._doc_type.refresh()
#'''
