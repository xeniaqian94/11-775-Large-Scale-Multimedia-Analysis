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

# Performs K-means clustering and save the model to a local file

if __name__ == '__main__':
    if len(sys.argv) != 5:
        print "Usage: {0} event_name feat_dir feat_dim output_file".format(sys.argv[0])
        print "event_name -- name of the event (P001, P002 or P003 in Homework 1)"
        print "feat_dir -- dir of feature files"
        print "feat_dim -- dim of features"
        print "output_file -- path to save the svm model"
        exit(1)

    event_name = sys.argv[1]
    feat_dir = sys.argv[2]
    feat_dim = int(sys.argv[3])
    output_file = sys.argv[4]

    train_list="list/"+event_name+"_train"
    X=np.asarray([])
    Y=[]
    pos_count=0
    neg_count=0
    libsvm_file=open("libsvm_train_file_"+event_name,"w")
    for line in open(train_list,"r"):
        audio_name=line.split(" ")[0]
        label=line.split(" ")[1].split("\n")[0]
        feat_vec=np.genfromtxt(feat_dir+audio_name,delimiter=";")
        if (label=="NULL"):
            label=0
            neg_count+=1
        elif (label==event_name):
            label=1
            pos_count+=1
        if len(X)==0:
            X=[feat_vec]
        else:
            X=np.append(X,[feat_vec],axis=0)
        Y=Y+[label]
        libsvm_file.write(str(label)+" ")
        for i in range(len(feat_vec)):

            libsvm_file.write(str(i+1)+":"+str(feat_vec[i])+" ")
        libsvm_file.write("\n")
    libsvm_file.close()

    print "Data loading finished positive "+str(pos_count)+" negative "+str(neg_count)
    assert (pos_count == 10 ),"10 positive instances"
    assert (neg_count == 200 ),"200 negative instances"
    # print Y,len(Y)
    #pipe_lrSVC = Pipeline([('scaler', StandardScaler()), ('clf', SVC(probability=True))])
    # pipe_lrSVC = Pipeline([('scaler', StandardScaler()), ('clf', LinearSVC())])
    # pipe_lrSVC.fit(X,Y)
    # pickle.dump(pipe_lrSVC,open(output_file+'.pickle','wb'))
    # lin_clf=SVC(verbose=True)
    #pipe_lrSVC.fit(X,Y,**{'clf__sample_weight':np.array([1.0/pos_count if i==0 else 1.0/neg_count for i in Y])})
    #print preprocessing.scale(X)
 #   print Y
    pipe_lrSVC=SVC(probability=True)
    pipe_lrSVC.fit(preprocessing.scale(X),Y) 
    #pipe_lrSVC.fit(preprocessing.scale(X),Y,sample_weight=np.array([1.0/pos_count if i==0 else 1.0/neg_count for i in Y]))
    pickle.dump(pipe_lrSVC,open(output_file+'.pickle','wb'))
    
    # y_pred = pipe_lrSVC.predict(X_test)
    print 'SVM trained successfully for event %s!' % (event_name)
