import numpy as np
import os
import cPickle
from sklearn.cluster.k_means_ import KMeans
import sys
import pickle
import re
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
# nltk.download()
stopwords_list=stopwords.words("english")
print "nltk download succeed! "

from nltk.stem.lancaster import LancasterStemmer
st = LancasterStemmer()

# Generate k-means features for videos; each video is represented by a single vector

if __name__ == '__main__':

	 if len(sys.argv) != 5:
			print "Usage: {0} file_list cluster_num".format(sys.argv[0])
			print "file_list -- the list of videos"
			print "cluster_num -- number of cluster"
			print "feature_name --name of feature, tf or tfidf"
			print "method asroutput or kaldi"
			exit(1)
	 method=sys.argv[4]
	 num_features=int(sys.argv[2])
	 feature_name=sys.argv[3]
	 vectorizer = CountVectorizer(analyzer = "word",   \
														 tokenizer = None,    \
														 preprocessor = None, \
														 stop_words = stopwords_list,   \
														 max_features = sys.maxint)

	 file_list = sys.argv[1]
	 feat_dir=method+"_"+str(num_features)+"_"+feature_name+"/"
	 print feat_dir
	 if (not os.path.exists(feat_dir)):
			os.mkdir(feat_dir)

	 index=0
	 # load the kmeans model

	 clean_train_reviews=[]
	 for line in open(file_list.replace("all.video","train_dev"),"r").readlines():
			index=index+1
			# print "data cleaning "+str(index)


			audio_name=line.split()[0]
			if not line.split()[1]=="NULL":
				text_file=method+"/"+audio_name+".txt"
				with open(text_file) as f:
					 linelist = [line.rstrip() for line in f]
				text=" ".join(linelist)
				letters_only=re.sub("[^a-zA-Z]"," ",text)  # The text to search
				# lower_case=letters_only.lower()
				lower_case=letters_only.lower()
				# print lower_case

				# words = [st.stem(word) for word in lower_case.split(" ")]

				words=lower_case.split()
				words = [w for w in words if not w in stopwords_list]

				words=[st.stem(w) for w in words]
				clean_train_reviews.append(" ".join(words))
	 print "Load text contents ready as a list of strings of length "+str(len(clean_train_reviews))
	 train_data_features = vectorizer.fit_transform(clean_train_reviews)

	 print "Take a look at the words in the vocabulary"
	 vocab = vectorizer.get_feature_names()
	 print len(vocab)


	 clean_train_reviews=[]
	 for line in open(file_list,"r").readlines():
			index=index+1
			# print "data cleaning "+str(index)


			audio_name=line.strip()
			text_file=method+"/"+audio_name+".txt"
			with open(text_file) as f:
				 linelist = [line.rstrip() for line in f]
			text=" ".join(linelist)
			letters_only=re.sub("[^a-zA-Z]"," ",text)  # The text to search
			lower_case=letters_only.lower()
			# lower_case=text.lower()
			# print lower_case

			# words = [st.stem(word) for word in lower_case.split(" ")]
			# print stopwords_list
			words=lower_case.split()
			words = [w for w in words if not w in stopwords_list]

			words=[st.stem(w) for w in words]
			clean_train_reviews.append(" ".join(words))
	 print "Load text contents ready as a list of strings of length "+str(len(clean_train_reviews))
	 train_data_features = vectorizer.transform(clean_train_reviews)
	 # print vectorizer.get_feature_names()
	 train_data_features = train_data_features.toarray()
	 # print train_data_features[0]

	 print "Counts of each vocabulary word within the dictionary"
	 # Sum up the counts of each vocabulary word
	 dist = np.sum(train_data_features, axis=0)
	 # print dist
	 # For each, print the vocabulary word and the number of times it 
	 # appears in the training set
	 print "Constuctuing dictionary"
	 ctf=[]
	 for tag, count in zip(vocab, dist):
			 # print count, tag
			 ctf=ctf+[count]

	 print len(train_data_features)
	 print train_data_features.shape
	 print len(train_data_features[0])
	 print train_data_features[0].shape
	 print len(ctf)
	 train_data_features=np.asarray(train_data_features,dtype=np.float32)

	 
	 if (feature_name=="tfidf"):
			totalWords=np.sum(dist)
			ctf=np.log(totalWords*1.0/np.asarray(ctf))
			print ctf
			print totalWords
			for i in range(len(train_data_features)):
				# if i==0:
				# 	print train_data_features[0]
				train_data_features[i]=np.multiply(list(train_data_features[i]),list(ctf))

			# 	if i==0:
			# 		print train_data_features[0]
			# print train_data_features[1]


	 audio_list=open(file_list,"r").readlines()
	 # print train_data_features

	 for index in range(len(audio_list)):
			audio_name=audio_list[index].strip()
			np.savetxt(feat_dir+audio_name,train_data_features[index],delimiter=';')
