import commands
from sklearn import preprocessing
import numpy as np
import os
from sklearn.svm.classes import SVC
from sklearn.svm import LinearSVC
import cPickle
import sys
import pickle
# Performs K-means clustering and save the model to a local file
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
if __name__ == '__main__':

    if len(sys.argv) != 5:
        print "Usage: {0} model_file feat_dir feat_dim output_file".format(sys.argv[0])
        print "model_file -- path of the trained svm file"
        print "feat_dir -- dir of feature files"
        print "feat_dim -- dim of features; provided just for debugging"
        print "output_file -- path to save the prediction score"
        exit(1)

    model_file = sys.argv[1]
    feat_dir = sys.argv[2]
    feat_dim = int(sys.argv[3])
    output_file = sys.argv[4]
    pipe_lrSVC=pickle.load(open(model_file+'.pickle','rb'))


    test_list="list/test.video"
    X=np.asarray([])

    for line in open(test_list,"r").readlines():
        #print line
        audio_name=line.split()[0]
        feat_vec=np.genfromtxt(feat_dir+audio_name,delimiter=";")
        if len(X)==0:
            X=[feat_vec]
        else:
            X=np.append(X,[feat_vec],axis=0)
    #print X
    Y=pipe_lrSVC.predict_proba(preprocessing.scale(X))

    #Y=pipe_lrSVC.predict(X)
    groundtruth_label="list/"+model_file.split(".")[1]+"_test_label"
    #print groundtruth_label
    Y_truth=[]

    for line in open(groundtruth_label,"r"):
        Y_truth+=[int(line.strip())]
    #print Y, Y_truth
    print model_file.split(".")[1]+" CLASS ACCURACY: "+str(accuracy_score(Y_truth,pipe_lrSVC.predict(preprocessing.scale(X))))
    fwrite=open(output_file,"w")
    for i in range(len(Y)):
        fwrite.write(str(Y[i][1])+"\n")
    fwrite.close()
    ap_output=commands.getstatusoutput("ap "+groundtruth_label+" "+output_file)

    print model_file.split(".")[1]+" MAP: "+ap_output[1].split(": ")[1]
    #print model_file.split(".")[1]+" MAP: "+ap_output.split(": ")[1]
