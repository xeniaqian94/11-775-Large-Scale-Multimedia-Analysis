#!/bin/python 

import numpy as np
import os
from sklearn.cluster.k_means_ import KMeans
# import cPickle
import pickle
import sys

# Performs K-means clustering and save the model to a local file

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print "Usage: {0} mfcc_csv_file cluster_num output_file".format(sys.argv[0])
        print "mfcc_csv_file -- path to the mfcc csv file"
        print "cluster_num -- number of cluster"
        print "output_file -- path to save the k-means model"
        exit(1)

    mfcc_csv_file = sys.argv[1]; output_file = sys.argv[3]
    cluster_num = int(sys.argv[2])
    mfcc_vectors=np.genfromtxt(mfcc_csv_file, delimiter=";")
    kmeans_model=KMeans(n_clusters=cluster_num, init='k-means++', n_init=10)
    

    kmeans_model.fit(mfcc_vectors)


    pickle.dump(kmeans_model,open('kmeans_model.pickle','wb'))
    print "K-means trained successfully!"
# create_kmeans.py

    mfcc_file="HVC2403.mfcc.csv"
    kmeans_model = pickle.load(open('kmeans_model.pickle', 'rb'))
    array=np.genfromtxt(mfcc_file, delimiter=";")
    print len(array)
    words=kmeans_model.predict(np.genfromtxt(mfcc_file, delimiter=";"))
    print "length of words in this audio "+str(len(words))

    print "words "+str(words)

    freq_per_cluster=np.bincount(words)
    print "freq_per_cluster "+str(len(freq_per_cluster))+" "+str(freq_per_cluster)
    non_zero_clusters=np.nonzero(freq_per_cluster)[0]
    print "non zero cluster freq "+str(zip(non_zero_clusters,freq_per_cluster[non_zero_clusters]))


