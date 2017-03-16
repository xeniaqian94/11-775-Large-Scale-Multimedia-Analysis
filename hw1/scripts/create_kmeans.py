import numpy as np
import os
import cPickle
from sklearn.cluster.k_means_ import KMeans
import sys
import pickle
# Generate k-means features for videos; each video is represented by a single vector

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print "Usage: {0} kmeans_model, cluster_num, file_list".format(sys.argv[0])
        print "kmeans_model -- path to the kmeans model"
        print "cluster_num -- number of cluster"
        print "file_list -- the list of videos"
        exit(1)

    kmeans_model = sys.argv[1]; file_list = sys.argv[3]
    cluster_num = int(sys.argv[2])

    # load the kmeans model
    kmeans_model = pickle.load(open(kmeans_model+'.pickle', 'rb'))
    print "K-means models loaded successfully!"
    feat_dir="mfcc_feature_"+str(cluster_num)+"/"
    if (not os.path.exists(feat_dir)):
        os.mkdir(feat_dir)
    index=0
    for line in open(file_list,"r").readlines():
        index=index+1
        
        audio_name=line.split("\n")[0]
        mfcc_file="mfcc/"+audio_name+".mfcc.csv"
        array=np.genfromtxt(mfcc_file, delimiter=";")
        print str(index)+" "+mfcc_file+" number of audio words "+str(len(array))
        words=kmeans_model.predict(np.genfromtxt(mfcc_file, delimiter=";"))
        freq_per_cluster=np.bincount(words,minlength=cluster_num)
        np.savetxt(feat_dir+audio_name,freq_per_cluster,delimiter=';')
