# Dependencies
from flask import Flask, request, jsonify,render_template

from sklearn.externals import joblib
import traceback
import pandas as pd 
import numpy as np
import nltk
import re
import numpy as np
from nltk import word_tokenize
from nltk.corpus import stopwords
from string import punctuation
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer
import re
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
import google_images_download 
import sys



#nltk.download()
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
stop_words = set(stopwords.words("english"))

# Your API definition
app = Flask(__name__)

import zipfile
with zipfile.ZipFile("glove.zip","r") as zip_ref:
    zip_ref.extractall()
import os
glove_dir = 'glove'
embeddings_index = {} # empty dictionary
f = open(os.path.join(glove_dir, 'glove.6B.50d.txt'), encoding="utf-8")
for line in f:
    values = line.split()
    word = values[0]
    coefs = np.asarray(values[1:], dtype='float32')
    embeddings_index[word] = coefs
f.close()

def read_p(data):
    text= data.split(". ")
    sentences = []
#         for i,sent in text:
    for sentence in text:
        sentences.append(sentence.replace("[^a-zA-Z]", " ").split(" "))
#             print(sentence)
    sentences.pop() 
    return sentences

def vectorizer(summ_data,embeddings_index):
    summ_vec={}
    count=1
    for list_w in summ_data:
        temp=[]
        for word in list_w:
            if word in embeddings_index.keys():
                temp.append(embeddings_index[word])
        summ_vec[count]=temp
        count=count+1
    return summ_vec

def word_binder_dict(vec):
    summ_sent_vec={}
    for num,list_w in vec.items():
        n=1
        temp=np.zeros(50)
        for word in list_w:
            temp=temp+word
            n=n+1
        summ_sent_vec[num]=(temp/n)
    return summ_sent_vec

def doc_binder(vec):
    temp=np.zeros(50)
    n=1
    for num,list_w in vec.items():
        temp=temp+list_w
        n=n+1
    doc_vec=(temp/n)
        
    return doc_vec

def dist_bw_sent_doc_norm2(vec1,vec2):
    dist_arr={}
    for num,sent in vec1.items():
        dist = np.linalg.norm(vec2-sent)
        dist_arr[num]=dist
    return dist_arr

def dist_bw_sent_doc_cos(vec1,vec2):
    dist_arr={}
    for num,sent in vec1.items():
        dist =cosine_distance(vec2,sent)
        dist_arr[num]=dist
    return dist_arr

def summarizer(doc_norm2_dist,joined_summ):
	summarize_text = []
	meaner=[]
	for i in range(1,len(doc_norm2_dist)+1):
		meaner.append(doc_norm2_dist[i])
	mean_arr=np.array(meaner)
	threshold=(mean_arr.mean()+np.median(mean_arr))/1.8
	# threshold=100
	for i in range(1,len(doc_norm2_dist)+1):
		if doc_norm2_dist[i]<threshold:
			summarize_text.append("".join(joined_summ[i]))
	return summarize_text

def corpus_maker(summarize_text):
    corpus = []
    for i in range(len(summarize_text)):
        #Remove punctuations
        text = re.sub('[^a-zA-Z]', ' ',summarize_text[i] )

        #Convert to lowercase
        text = text.lower()

        #remove tags
        text=re.sub("&lt;/?.*?&gt;"," &lt;&gt; ",text)

        # remove special characters and digits
        text=re.sub("(\\d|\\W)+"," ",text)

        ##Convert to list from string
        text = text.split()

        ##Stemming
        ps=PorterStemmer()
        #Lemmatisation
        lem = WordNetLemmatizer()
        text = [lem.lemmatize(word) for word in text if not word in  
                stop_words] 
        text = " ".join(text)
        corpus.append(text)
    return corpus 


def get_top_n_words(corpus, n=None):
    vec = CountVectorizer().fit(corpus)
    bag_of_words = vec.transform(corpus)
    sum_words = bag_of_words.sum(axis=0) 
    words_freq = [(word, sum_words[0, idx]) for word, idx in      
                   vec.vocabulary_.items()]
    words_freq =sorted(words_freq, key = lambda x: x[1], 
                       reverse=True)
    return words_freq[:n]

def get_top_n2_words(corpus, n=None):
    vec1 = CountVectorizer(ngram_range=(2,2),  
            max_features=2000).fit(corpus)
    bag_of_words = vec1.transform(corpus)
    sum_words = bag_of_words.sum(axis=0) 
    words_freq = [(word, sum_words[0, idx]) for word, idx in     
                  vec1.vocabulary_.items()]
    words_freq =sorted(words_freq, key = lambda x: x[1], 
                reverse=True)
    return words_freq[:n]

def get_top_n3_words(corpus, n=None):
    vec1 = CountVectorizer(ngram_range=(3,3), 
           max_features=2000).fit(corpus)
    bag_of_words = vec1.transform(corpus)
    sum_words = bag_of_words.sum(axis=0) 
    words_freq = [(word, sum_words[0, idx]) for word, idx in     
                  vec1.vocabulary_.items()]
    words_freq =sorted(words_freq, key = lambda x: x[1], 
                reverse=True)
    return words_freq[:n]

def generate_summ_key(path):
	summ_data= read_p(path)
	joined_summ={}
	n=0

	for list_w in summ_data:
		n=n+1
		text=' '.join(list_w)
		joined_summ[n]=text
	summ_vec=vectorizer(summ_data,embeddings_index)
	summ_sent_vec=word_binder_dict(summ_vec)
	doc_vec=doc_binder(summ_sent_vec)
	doc_cos_dist=dist_bw_sent_doc_cos(summ_sent_vec,doc_vec)
	doc_norm2_dist=dist_bw_sent_doc_norm2(summ_sent_vec,doc_vec)

	summarize_text=summarizer(doc_norm2_dist,joined_summ)
		
	stop_words = set(stopwords.words("english"))
		
	corpus=corpus_maker(summarize_text)
	cv=CountVectorizer(max_df=1,stop_words=stop_words, max_features=10000, ngram_range=(1,3))
	X=cv.fit_transform(corpus)

	n=5

	top_words = get_top_n_words(corpus, n)
	top_df = pd.DataFrame(top_words)
	top_df.columns=["Word", "Freq"]

	keyword=[]

	for word in top_df['Word']:
		keyword.append(word)

	top2_words = get_top_n2_words(corpus, n)
	top2_df = pd.DataFrame(top2_words)
	top2_df.columns=["Bi-gram", "Freq"]
	top2_df['Bi-gram']

	bi=[]

	for word in top2_df['Bi-gram']:
		keyword.append(word)

	top3_words = get_top_n3_words(corpus, n)
	top3_df = pd.DataFrame(top3_words)
	top3_df.columns=["Tri-gram", "Freq"]

	tri=[]

	for word in top3_df['Tri-gram']:
		keyword.append(word)
		
	return summarize_text,keyword
# @app.route("/")
# def index():
#     return render_template("index.html")
@app.route('/list_add', methods=['GET','POST'])
def list_add():
	# return "hello"
    #print("Before JSON")
	text = request.get_json()
	# print(text)
	# r="The tiger is the largest extant cat species and a member of the genus Panthera. It is most recognisable for its dark vertical stripes on orange-brown fur with a lighter underside. It is an apex predator, primarily preying on ungulates such as deer and wild boar."
	r=text['data']
	# print(r)
    #print("This is where i am")
    #sys.stdout.flush()
	a,b=generate_summ_key(r)
	response = google_images_download.googleimagesdownload() 
	search_queries = []

	for contents in b:
		search_queries.append(contents)



	def downloadimages(query): 
		# keywords is the search query 
		# format is the image file format 
		# limit is the number of images to be downloaded 
		# print urs is to print the image file url 
		# size is the image size which can 
		# be specified manually ("large, medium, icon") 
		# aspect ratio denotes the height width ratio 
		# of images to download. ("tall, square, wide, panoramic") 
		arguments = {"keywords": query, 
					"format": "jpg", 
					"limit":1, 
					"print_urls":True, 
					"size": "medium", 
					"aspect_ratio": "panoramic"} 
		try: 
			response.download(arguments) 
		
		# Handling File NotFound Error   
		except FileNotFoundError: 
			arguments = {"keywords": query, 
						"format": "jpg", 
						"limit":1, 
						"print_urls":True, 
						"size": "medium"} 
						
			# Providing arguments for the searched query 
			try: 
				# Downloading the photos based 
				# on the given arguments 
				response.download(arguments)
			except: 
				pass

	# Driver Code 
	# orig_stdout = sys.stdout
	# f = open('purang_dega.txt', 'w+')
	# sys.stdout = f
	# print (1234)
	links=[]
	for query in search_queries:
		downloadimages(query)
		links.append(query)
	f = open("keywords.txt", "r")
	
	# print (1234)
	# if f.mode=="r":
		# contents = f.read()
		# links.append(contents)
	p=''
	# print (1234)
	for i in a:
		# p = i + '.'+''.join(prev)
		p=p+'.'+i
	output= p+'  %42069420%  ' + ' '.join(links)
	# print (1234)
	return output

# @app.route('/wow', methods=['POST'])
# def wow():
# 	a=[1,2,3]
# 	return "a"

if __name__ == "__main__":
    app.debug=True
#     app.run()





