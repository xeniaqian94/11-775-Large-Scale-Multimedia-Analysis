#!/bin/python 

import numpy as np 
import os
from sklearn.cluster.k_means_ import KMeans
import cPickle
import sys
import pickle 
# Performs K-means clustering and save the model to a local file

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print "Usage: {0} mfcc_csv_file cluster_num output_file".format(sys.argv[0])
        print "mfcc_csv_file -- path to the mfcc csv file"
        print "cluster_num -- number of cluster"
        print "output_file -- path to save the k-means model"
        exit(1)

    mfcc_csv_file = sys.argv[1]; 
    output_file = sys.argv[3]
    cluster_num = int(sys.argv[2]) 
    
    mfcc_vectors=np.genfromtxt(mfcc_csv_file, delimiter=";")
    kmeans_model=KMeans(n_clusters=cluster_num, init='k-means++', n_init=10,verbose=1)
    kmeans_model.fit(mfcc_vectors)
    pickle.dump(kmeans_model,open(output_file+'.pickle','wb'))

    print "K-means trained successfully!"
