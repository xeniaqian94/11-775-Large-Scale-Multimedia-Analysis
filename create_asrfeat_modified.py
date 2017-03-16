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



# Generate k-means features for videos; each video is represented by a single vector

if __name__ == '__main__':

   # python scripts/create_asrfeat.py vocab list/all.video
   # print "Usage: {0} vocab_file, file_list".format(sys.argv[0])
   #      print "vocab_file -- path to the vocabulary file"
   #      print "file_list -- the list of videos"
   if len(sys.argv) != 4:
      print "Usage: {0} file_list cluster_num".format(sys.argv[0])
      print "file_list -- the list of videos"
      print "cluster_num -- number of cluster"
      print "feature_name --name of feature, tf or tfidf"
      
      exit(1)

   num_features=int(sys.argv[2])
   feature_name=sys.argv[3]
   vectorizer = CountVectorizer(analyzer = "word",   \
                             tokenizer = None,    \
                             preprocessor = None, \
                             stop_words = None,   \
                             max_features = num_features) 

   file_list = sys.argv[1]
   feat_dir="asroutput_"+str(num_features)+"_"+feature_name+"/"
   if (not os.path.exists(feat_dir)):
        os.mkdir(feat_dir)
  
   index=0
   # load the kmeans model
   clean_train_reviews=[]
   for line in open(file_list,"r").readlines():
      index=index+1
      print "data cleaning "+str(index)
      audio_name=line.strip()
      text_file="asroutput/"+audio_name+".txt"
      with open(text_file) as f:
         linelist = [line.rstrip() for line in f]
      text=" ".join(linelist)
      letters_only=re.sub("[^a-zA-Z]"," ",text)  # The text to search
      lower_case=letters_only.lower()
      words=lower_case.split()
      words = [w for w in words if not w in stopwords_list]
      clean_train_reviews.append(" ".join(words))
   print "Load text contents ready as a list of strings of length "+str(len(clean_train_reviews))
   train_data_features = vectorizer.fit_transform(clean_train_reviews)
   train_data_features = train_data_features.toarray()
   # print train_data_features[0]

   print "Take a look at the words in the vocabulary"
   vocab = vectorizer.get_feature_names()
   print vocab

   print "Counts of each vocabulary word within the dictionary"
   # Sum up the counts of each vocabulary word
   dist = np.sum(train_data_features, axis=0)
   print dist 



   # For each, print the vocabulary word and the number of times it 
   # appears in the training set
   print "Constuctuing dictionary"
   ctf=[]
   for tag, count in zip(vocab, dist):
       print count, tag
       ctf=ctf+[count]

   if (feature_name=="tfidf"):
      totalWords=np.sum(dist)
      train_data_features=[a*np.log(totalWords*1.0/b) for a,b in zip(train_data_features,ctf)]
   

   audio_list=open(file_list,"r").readlines()
   for index in range(len(audio_list)):
      audio_name=audio_list[index].strip()
      print "extract features for each file "+str(index)+" "+audio_name+" "+str(np.count_nonzero(train_data_features[index]))
        # print train_data_features[index]
        # freq_per_cluster=np.bincount(words,minlength=cluster_num)
      np.savetxt(feat_dir+audio_name,train_data_features[index],delimiter=';')
    # read in each txt file



    #based on vocab create a tf/tf-idf vector,save as convension 
    
    # kmeans_model = pickle.load(open(kmeans_model+'.pickle', 'rb'))
    # print "K-means models loaded successfully!"
    # feat_dir="mfcc_feature_"+str(cluster_num)+"/"
    # if (not os.path.exists(feat_dir)):
    #     os.mkdir(feat_dir)
    
    