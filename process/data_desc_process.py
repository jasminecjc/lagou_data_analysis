# -*- coding: utf-8 -*-
import jieba
import os
from collections import Counter
import codecs

file_list = ['data_visualize.txt', 'data_analysis.txt', 'data_arc.txt', 'data_mining.txt', 'data_dev.txt']
_curpath=os.path.normpath( os.path.join( os.getcwd(), os.path.dirname(__file__) ))
settings_path = os.environ.get('dict.txt')
if settings_path and os.path.exists(settings_path):
    jieba.set_dictionary(settings_path)
elif os.path.exists(os.path.join(_curpath, 'data/dict.txt.big')):
    jieba.set_dictionary('data/dict.txt.big')
else:
    print "Using traditional dictionary!"

dic = open('dict.txt', 'r')
dic_list = []
while 1:
    line = dic.readline().decode('utf-8').strip()
    dic_list.append(line)
    if not line:
        break
    pass
for file in file_list:
    with codecs.open('../spider/' + file, "r",encoding='utf-8', errors='ignore') as string:
        string = string.read().upper()
        res = jieba.cut(string, HMM=False)
        reslist = list(res)
        wordDict = {}
        for i in reslist:
            if i not in dic_list:
                continue
            if i in wordDict:
                wordDict[i]=wordDict[i]+1
            else:
                wordDict[i] = 1
    count = Counter(wordDict)
    word_res = count.most_common()[:50]
    f_out = open('word_%s'%(file), 'wt')
    for word in word_res:
        f_out.write(word[0].encode('utf-8') + '  ' + str(word[1]) + '\n')
    f_out.close()


