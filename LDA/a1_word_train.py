from nltk import corpus
import gensim as gensim
from nltk.tokenize import RegexpTokenizer
#from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import gensim

tokenizer = RegexpTokenizer(r'\w+')

# create English stop words list
en_stop = ['if ', 'why', 'down ', "you'll", 'mightn', 'because', "needn't", ' him ', ' some ', "wouldn't", "shouldn't", 'over ', 'ours', 'again', 'under', 'few ', 'isn ', 'above', "you've", ' is ', ' be', 'themselves', 'itself', ' than ', 'there', ' up ', ' all ', ' on ', 'can', 'couldn', 'or ', ' no ', 'until', "weren't", 'weren', 'through', ' are ', ' you ', "couldn't", ' re ', 'while', 'about', "shan't", 'here ', 'now ', 'out ', "should've", "doesn't", ' she ', 'where', 'will', "aren't", ' not ', "won't", ' her ', ' t ', 'whom', 'yourself', 'have', ' me ', 'any ', 'nor ', ' has ', 'having', "she's", 'being', 'wasn', ' he ', "wasn't", ' ll ', "haven't", 'they ', 'it ', 'were', 'below', 'own', ' in  ', 'should', ' an ', 'shan', "don't", ' we ', 'who ', 'when ', 'shouldn', ' wouldn ' , ' at ', ' them ', 'further', 'once', ' as ', 'these', ' am ', ' with ', ' to ', 'myself', ' a ', 'and ', "you're", 'that', 'after', 'needn', 'aren', 'yours', "it's", 'hadn', 'haven', 'their', 'the ', ' ain ', "hadn't", 'been', "isn't", 'other', 'mustn', ' don ', 'which', "that'll", 've ', "you'd", ' d ', 'both', 'off', ' o ', 'ourselves', 'but ', 'doesn ', 'from ', "hasn't", 'then ', 'those ', 'himself', 'do ', 'how ', 'each ', 'this ', 'only', 'against', 'between', 'hasn', 'theirs', 'was ', 'my ', 'hers', ' y ', ' s ', 'just', 'his', 'had', "mightn't", 'too', 'doing', 'same', 'very', ' so ', ' ma ', 'before', 'won', ' did ', ' for ', 'into', 'didn', ' i ', 'during', "mustn't", 'herself', 'yourselves', 'what', 'does', 'most', 'such', 'our ', ' m ', 'your', ' by ', ' its ', "didn't", ' of ', ' more ']

# Create p_stemmer of class PorterStemmer
p_stemmer = PorterStemmer()

# create sample documents
doc_a = "Brocolli is good to eat. My brother likes to eat good brocolli, but not my mother."
doc_b = "My mother spends a lot of time driving my brother around to baseball practice."
doc_c = "Some health experts suggest that driving may cause increased tension and blood pressure."
doc_d = "I often feel pressure to perform well at school, but my mother never seems to drive my brother to do better."
doc_e = "Health professionals say that brocolli is good for your health."

# compile sample documents into a list
doc_set = [doc_a, doc_b, doc_c, doc_d, doc_e]

# list for tokenized documents in loop
texts = []

# loop through document list
for i in doc_set:

    # clean and tokenize document string:清理并标记文档字符串
    raw = i.lower()
    tokens = tokenizer.tokenize(raw)

    # remove stop words from tokens-从标记中删除停止词
    stopped_tokens = [i for i in tokens if not i in en_stop]

    # stem tokens
    stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]
    print(stemmed_tokens)

    # add tokens to list:将令牌添加到列表中
    texts.append(stemmed_tokens)
    #print(texts.append(stemmed_tokens))
print(texts)
#查询文档（我这里是文献的数目）
M = len(doc_set)
print('文本数目：%d个' % M)

#----------------------------------------LDA部分-----------------------------------------
#利用 gensim 库构建文档-词频矩阵
import gensim
from gensim import corpora
#构建字典，把刚刚处理好的词都存进去
# turn our tokenized documents into a id <-> term dictionary
#将标记化文档转换为id<->术语词典
print("构建字典，把刚刚处理好的词都存进去-------------")
texts = [['differ brain region simultan'],['analyz individu differ','electroencephalogram(eeg) network','collaps network'],['stochast block model(sbm) result','made base','differ brain region simult',
         'analyz individu differ'] ,['collaps network','stochast block model\(sbm\) result','made base'],['partial interdepend network','starlik non structur','fulli interdepend network']]
# texts = [['brocolli', 'is', 'good', 'to', 'eat', 'my', 'brother', 'like', 'to', 'eat', 'good', 'brocolli', 'but', 'not', 'my', 'mother']]
dictionary = corpora.Dictionary(texts)
print("词典长度：",len(dictionary))
print("词典",dictionary)

# convert tokenized documents into a document-term matrix
#将标记化文档转换为文档术语矩阵
corpus = [dictionary.doc2bow(text) for text in texts]
print("文档-词频矩阵长度：",len(corpus))
print("文档-词频矩阵：",corpus)

#转换成文档词频稀疏矩阵
print("转换成文档词频----->稀疏矩阵")
from gensim.matutils import corpus2dense
corpus_matrix=corpus2dense(corpus, len(dictionary))
corpus_matrix.T
print(corpus_matrix.T)

#使用gensim来创建 LDA 模型对象
print("创建 LDA 模型对象------------------------")
Lda = gensim.models.ldamodel.LdaModel
#在文档-词频矩阵上运行和训练 LDA 模型
num_topics = 5#主题个数，参数可修改
# num_words  = 10#主题词个数
ldamodel = Lda(corpus, num_topics=num_topics, id2word=dictionary, passes=100000)#修改超参数，主题个数，遍历次数
doc_topic = [doc_t for doc_t in ldamodel[corpus]]
print('文档-主题矩阵:\n')
print(doc_topic)
print(doc_topic[0:19])

# for doc_topic in ldamodel.get_document_topics(corpus):
#     print(doc_topic)
print('主题-词:\n')
for topic_id in range(num_topics):
    print('Topic', topic_id)
    print(ldamodel.show_topic(topic_id))
    #print(ldamodel.show_topic(topic_id),topic_id)

# for idx, topic in ldamodel.print_topics():
#     print('Topic: {} Word: {}'.format(idx, topic))

# print(ldamodel.print_topics(num_topics=2, num_words=4))

#
print("使用TF-IDF运行LDA---------------------")
from gensim import corpora, models
tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]
from pprint import pprint
for doc in corpus_tfidf:
    pprint(doc)
    break

# lda_model_tfidf = gensim.models.LdaMulticore(corpus_tfidf, num_topics=10, id2word=dictionary, passes=20, workers=4)
# for idx, topic in lda_model_tfidf.print_topics(-1):
#     print('Topic: {} Word: {}'.format(idx, topic))
