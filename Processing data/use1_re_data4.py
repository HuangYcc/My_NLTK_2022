import os
os.chdir(r'../prepared')

import unidecode
from nltk.tokenize import word_tokenize   #分词
from nltk.stem import PorterStemmer       #词干化

# def replaceFomat(text: str, word: str, n: int,reverse=False):
#     '''对文本中的指定单词进行格式化的替换/替回
#     text-要替换的文本
#     word-目标单词
#     n-目标单词的序号
#     reverse-是否进行替回
#     Return:
#     ---
#     new_text-替换后的文本
#     '''
#     # 构造【中间变量】
#     new_text = text[ : ]
#     fmt = "<{}>".format(n)
#     # 替换
#     if reverse is False:
#         new_text = new_text.replace(word, fmt)  # 格式化替换
#         return new_text
#     # 替回
#     elif reverse is True:
#         new_text = new_text.replace(fmt, word)  # 去格式化替换
#         return new_text
#     # 要求非法，引发异常
#     else:
#         raise TypeError


# 替换成 ###
def replace_to_symbol(text: str, olds: list, symbol: str):
    '''一次替换多组字符串
    text-要替换的文本
    olds-旧字符串列表
    news-新字符串
    Return:
    ---
    new_text: str-替换后的文本
    '''

    for old in olds:
        text = text.replace(old, symbol)
        # print(1000)
        # print('###:', old, symbol)
    # print('替换后文本:', text)

    # 返回替换好的文本
    return text


import re
import pandas as pd
import numpy as np
#扩写
from nltk import data


# def expand_abbr(sen, abbr):
#     abbr=abbr.strip()
#     lenabbr = len(abbr)
#     ma = ''
#     #ind=text.index('( %s )'%abbr)
#     #if ind > 100:
#     #    sen=sen[ind-100:ind]
#
#     for i in range(0, lenabbr):
#         ma += abbr[i] + ".*" + ' '
#     #print ('ma:', ma)
#     #ma+='\('
#     ma = ma.strip(' ')
#     ma+='(?=\()'
#     p = re.findall(ma,sen,re.M)
#     if len(p)!=0:
#         return p[0]
#     else:
#         mat=''
#         for m in range(0, lenabbr-1):
#             mat+=abbr[m]+'.*'
#         mat+=abbr[-1]+'.* '
#         print(mat)
#         r=re.findall(mat+'(?=\()',sen,re.M)
#         if len(r)!=0:
#             return r[0]
#         else:
#             return ''


# 去掉括号里的长句
def expand_abbr(text, sen_list):
    '''
    :param text: 待处理文本
    :param sen_list: 匹配到的在括号里得到的列表
    :return:
    '''
    short_list = []
    long_list = []
    for sen in sen_list:
        # 去掉长句
        # sen = sen.strip()
        if ' ' in sen[1:-1] and len(sen) > 10:
            sen = '(' + sen + ')' # 拼接成完成长句
            long_list.append(sen)
            # print('long_list:', long_list)
            print(sen)
            text = text.replace(sen , '')
            print(text)
        else:
            print("sen:", sen)
            if len(sen.strip()) <= 2:
                long_list.append(sen)
            else:
                first = sen.strip()[0]
                # print(first)
                try:
                    # sen_short = re.findall(f' (%s.*?\(%s\))'%(first, sen), text, re.S)
                    sen_short = re.findall(' (%s.{1,100}?\(%s\))'%(first,sen), text, re.S|re.I)
                    print('sen_short:', sen_short)
                    # if not sen_short:
                    short_list.append(sen_short[0])
                except Exception as e:
                    print('error:', e)



    # print('short_list:', short_list)
    # 返回处理好的文本，和缩合扩写词
    return text, short_list, long_list


if __name__ == '__main__':
    fn=os.listdir('原始数据')
    fn = [float(i.replace('.txt','')) for i in fn]
    fn = [str(i) + '.txt' for i in sorted(fn)]
    print(fn)
    # exit()

    # 遍历文件
    times = 10
    for fff in fn:
        print('正在处理',fff)
        name=fff.replace('.txt','')
        try:
            with open("原始数据/%s.txt"%name,"r") as f1:
                accented_string=f1.read()
                #1.音译化完成##########################
                unaccented_string = unidecode.unidecode(accented_string)
                # print(accented_string,"\n",unaccented_string)
                #print("音译化完成")
        except:
            with open("原始数据/%s.txt"%name,"r",encoding='utf-8') as f1:
                accented_string=f1.read()
                #1.音译化完成##########################
                unaccented_string = unidecode.unidecode(accented_string)
                # print(accented_string,"\n",unaccented_string)
                #print("音译化完成")


        #2.文本词干化--完成######################
        word_tokens = word_tokenize(unaccented_string)   #分词
        filtered_sentence = [w for w in word_tokens]
        # print(" ".join(word_tokens))
        # print(" ".join(filtered_sentence))



        Stem_words = []
        ps =PorterStemmer()
        for w in filtered_sentence:
            rootWord=ps.stem(w)
            Stem_words.append(rootWord)
        print(filtered_sentence)
        print(Stem_words)
        # 写入cg 数据
        with open("cg数据\cg_%s.txt"%name,"w",encoding="utf-8") as f:
            for i in Stem_words :
                f.write(i+" ")
        print("文本词干化--完成")


        # 读取词干化文本
        with open('cg数据/cg_%s.txt'%name, 'r',encoding="utf-8") as file:
            text=file.read()
            print('cg_%s.txt'%name)
            print(text)

        '''需要替换的文本'''
        st = [' if ', ' why', ' down ', " you'll ", ' mightn ', ' because ', " needn't", ' him ', ' some ', "wouldn't", "shouldn't", 'over ', ' ours ', ' again ', 'under', ' few ', 'isn ', 'above', "you've", ' is ', ' be', 'themselves', 'itself', ' than ', 'there', ' up ', ' all ', ' on ', 'can', 'couldn', ' no ', 'until', "weren't", 'weren', 'through', ' are ', ' you ', "couldn't", ' re ', 'while', 'about', "shan't", 'here ', 'now ', 'out ', "should've", "doesn't", ' she ', 'where', 'will', "aren't", ' not ', "won't", ' her ', ' t ', 'whom', 'yourself', 'have', ' me ', 'any ', 'nor ', ' has ', 'having', "she's", 'being', 'wasn', ' he ', "wasn't", ' ll ', "haven't", 'they ', ' it ', 'were', 'below', 'own', ' in  ', 'should', ' an ', 'shan', "don't", ' we ', 'who ', 'when ', 'shouldn', ' wouldn ' , ' at ', ' them ', 'further', 'once', ' as ', 'these', ' am ', ' with ', ' to ', 'myself', ' a ', 'and ', "you're", 'that', 'after', 'needn', 'aren', 'yours', " it 's", 'hadn', 'haven', 'their', 'the ', ' ain ', "hadn't", 'been', "isn't", 'other', 'mustn', ' don ', 'which', "that'll", 've ', "you'd", ' d ', 'both', 'off', ' o ', 'ourselves', 'but ', 'doesn ', 'from ', "hasn't", 'then ', 'those ', 'himself', 'do ', 'how ', 'each ', 'this ', 'only', 'against', 'between', 'hasn', 'theirs', 'was ', 'my ', 'hers', ' y ', ' s ', 'just', 'his', 'had', "mightn't", 'too', 'doing', 'same', 'very', ' so ', ' ma ', 'before', 'won', ' did ', ' for ', 'into', 'didn', ' i ', 'during', "mustn't", 'herself', 'yourselves', 'what', 'does', 'most', 'such', 'our ', ' m ', 'your', ' by ', ' its ', "didn't", ' of ', ' more ']
        olds = ["The ", "A ", " of "," for "," the ","It "," is "," or ","In "," to ","a "," that "," become"," ha "," between "," not "," have "," should ","FORMULA","and "," in ","at "," a ",
                "In ","as ","REF "," it "," we "," an ","which"," are "," an "," two "," been"," us "," they"," on "," becom"," been"," also "," be ","just","each","either","when","'ve","ve "," t ","``","'",
                " then "," enabl "," above "," according "," actually "," after "," again "," n "," against ","agrave","all "," allow "," almost "," along "," alpha ","already","also","although","always"," am ","among",
                " an " , ' section ', ' ref '," and "," another"," any "," anybody "," are ","Thus"," was "," thi ",' much ','(X)', ".",",",":"]
        #特殊符号
        text_String=['MAINCIT','FIGURE','CIT ','FORMULA','Ref.','cit '," e.g."]
        _number = ["<<",">>"]
        olds = olds+st+text_String+_number
        ''''''
        # 实现替换
        new = " ### "
        result = replace_to_symbol(text, olds, new)  # 实现了替换
        print('替换后文本:', result)

        # 写入fc数据
        with open("fc数据/fc_%s.txt"%name,'w') as f:
            for i in result.split('###'):
                i = i.strip()
                if len(i)>1 :
                    # print('555:', i)
                    if '(' in i and ')' not in i:
                        i = i.replace('(', '')
                    if '(' not in i and ')' in i:
                        i = i.replace(')', '')
                    f.write(i.strip()+'\n')
                    #print(i)
                    #print(len(i))
            print('输出成功，分词词组形式出现fc.txt....')

        #读取存在空行的文件，删除其中的空行，并将其保存到新的文件中
        with open("fc数据/fc_%s.txt"%name,'r',encoding = 'utf-8') as fr, open("a_del数据/a_del_%s.txt"%name,'w',encoding = 'utf-8') as fd:
            for text in fr.readlines():
                if text.split():
                    fd.write(text.strip()+'\n')#删除开头和结尾空格

            print('输出成功，删除删除开头和结尾空格a_del.txt....')

        # 删除单个单词，如果空格为0则为单个单词--->删除
        with open("a_del数据/a_del_%s.txt"%name,'r',encoding="utf-8") as f:
            with open('result数据/result1_%s.txt'%name,'w') as f1:
                for line in f.readlines():
                    # space_counts = 0
                    # space_counts += len(line.split())
                    # num=space_counts-1
                    # print(num)
                    # 单词长度大于1，就写入
                    # if num > = 1 :
                    if ' ' in line.strip():
                        # print(line)
                        f1.write(line)






        # 读取result数据
        with open('result数据/result1_%s.txt'%name,'r',encoding="utf-8") as f:
            text_line=[i.strip() for i in f.readlines()]
            text=' '.join(text_line)
            # 匹配到的括号里词组
            use_text = re.findall("\((.*?)\)", text, re.S)

            # print(use_text)
            # print(len(use_text))
            # for i in range(len(use_text)):
            #     if use_text[i].lower() not in dic.keys():
            #         r=expand_abbr(text, use_text[i].lower())
            #         dic.update({use_text[i].lower():r})
            # print(dic)
            dic={}
            # 返回后的文本和匹配到的缩写词
            text, short_list, long_list = expand_abbr(text, use_text)
            for short in short_list:
                short = short.split('(')
                key = short[0].strip()
                value = short[1].strip()
                dic.update({key: value})
            # text_line = [text]

        # 写入字典
        with open(r'词典\cidian_%s.txt'%name,'wt',encoding="utf-8") as f4:
            for item in dic.items():
                f4.write(item[0].strip())
                f4.write(',')
                f4.write(item[1].replace(')', '').strip())
                f4.write('\n')

        _dic = {}
        with open(r'词典\cidian_%s.txt'%name,'r',encoding="utf-8") as ddd:
            dic_list=ddd.readlines()
            for dr in dic_list:
                dr=dr.replace('\n','')
                drs=dr.split(',')
                _dic.update({drs[0]:drs[1]})

        with open(r'扩词后结果\result_%s.txt'%name,'wt',encoding="utf-8") as f2:
            with open(r'扩词结果加文件名\result_%s.txt'%name,'wt')  as f3:
                for hh in text_line:
                    for long in long_list:
                        hh = hh.replace(long, '')
                    hh=hh.replace('\n','')
                    hh=hh.strip()
                    for dc in _dic.items():
                        dc0=dc[0].strip()  # 缩写
                        dc1=dc[1].strip()
                        if dc1 in hh:  #  and dc0 not in hh
                            hh=hh.replace(dc1,dc0+'('+dc1+')')  # smpt --》 smapsatsd(smpt)
                            hh = hh.replace('( '+dc0+'('+dc1+')'+' )', f'({dc1})')
                    f2.write(hh)
                    f2.write('\n')
                    # print('long_list', long_list)
                    for long in long_list:
                        # print('111:', long)
                        hh = hh.replace(long, '')
                    f3.write(hh)
                    f3.write(',%s'%name+"\n")

        with open(r'扩词后结果\result_%s.txt'%name,'r',encoding="utf-8") as r:
            with open('san/result_%s.txt'%name,'w',encoding="utf-8") as rr:
                text = r.readlines()
                # text = sorted(text, key=lambda i: len(i))
                text = [i.strip() + '*%s'%name + '\n' for i in text]
                print(text)
                if len(text)>=3:
                    new = [i for i in text if len(i)>10 and not '.' in i]
                    if len(new) >= 3:
                        rr.write(new[-3]+new[-2]+new[-1])
                    else:
                        rr.write(text[-3]+text[-2]+text[-1])

                elif len(text)==2:
                    rr.write(text[-2]+text[-1])
                elif len(text)==1:
                    rr.write(text[-1])
                else:
                    continue
                print("取分词后的最后三个短句....")

                # x='('
                # y=')'
                # for t in text:
                #     print(t)
                #     if (((x in t)&(y not in t))|((y in t)&(x not in t))):
                #         print(t.find(x))
                #         text.remove(t)
                #         print("111")
                # print(text)
        # times -= 1
        # if not times:
        #     break




