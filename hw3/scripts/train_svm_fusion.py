from sklearn.calibration import CalibratedClassifierCV
from sklearn import preprocessing
import numpy as np
import os
from sklearn.svm.classes import SVC
from sklearn.svm import LinearSVC
import cPickle
import sys
import pickle
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


import itertools

import sklearn

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

from brew.base import Ensemble, EnsembleClassifier
from brew.stacking.stacker import EnsembleStack, EnsembleStackClassifier
from brew.combination.combiner import Combiner



def import_imtraj_txt(file_path):

    imtraj_line = (open(file_path,"r").readlines()[0]).strip()

    fields = imtraj_line.split(' ')
    field_tuples = [x.split(':') for x in fields]

    # The sparse vector position is 1 based
    num_fields = [ (int(x[0])-1, np.float(x[1])) for x in field_tuples]

    new_vect = np.zeros(32768)
    for field_id, field_val in num_fields:
        new_vect[field_id] = field_val

    return new_vect

def import_sift_txt(file_path):
    new_vect=np.zeros(128)
    return new_vect

def import_cnn_txt(file_path):
    new_vect=np.zeros(4096)
    return new_vect


if __name__ == '__main__':
    if len(sys.argv) != 5:
        print "Usage: {0} event_name round_num feat_dir output_file".format(sys.argv[0])
        print "event_name -- name of the event (P001, P002 or P003 in Homework 1)"
        print "round_num 0,1,2?"
        print "feat_dir -- dir of feature files"
        
        print "output_file -- path to save the svm model train_file_P00X_Xround_imtraj/SIFT/CNN"
        exit(1)


    event_name = sys.argv[1]
    round_num=sys.argv[2]
    feat_dir = sys.argv[3]
    output_file = sys.argv[4] 
    if not round_num=="all":
        rount_num=int(round_num)
        train_list="list/"+event_name+"_train_"+str(round_num)
    else:
    	train_list="list/train_dev"
    
    X=np.asarray([])
    Y=[]
    pos_count=0
    neg_count=0
    count=0
    print train_list,feat_dir
    for line in open(train_list,"r"):
        audio_name=line.split(" ")[0]
        # print audio_name
        count=count+1
 #       if (count%100==0):
#	    print count
        label=line.split(" ")[1].split("\n")[0]
        if "imtraj" in feat_dir: 
            feat_vec=import_imtraj_txt(feat_dir+audio_name+".spbof")
        else:
            feat_vec=np.genfromtxt(feat_dir+audio_name,delimiter=";")
        if (label==event_name):
            label=1
            pos_count+=1
        else:
            label=0
            neg_count+=1
        if len(X)==0:
            # print feat_vec,np.sum(feat_vec)
            X=[feat_vec]
        else:
            # print feat_vec,np.sum(feat_vec)
            X=np.append(X,[feat_vec],axis=0)
        Y=Y+[label]
    
    print "Data loading finished positive "+str(pos_count)+" negative "+str(neg_count)
    #pipe_lrSVC=SVC(C=10,gamma=0.0001,probability=True)

    clf1 = LogisticRegression(random_state=0)
    clf2 = RandomForestClassifier(random_state=0)
    #clf1 = SVC(kernel='linear',probability=True)
    #clf2 = SVC(kernel='poly',probability=True)
    clf3 = SVC(kernel='rbf',probability=True)

    # Creating Ensemble
    ensemble = Ensemble([clf1, clf2, clf3])
    eclf = EnsembleClassifier(ensemble=ensemble, combiner=Combiner('mean'))

    # Creating Stacking
    layer_1 = Ensemble([clf1, clf2, clf3])
    layer_2 = Ensemble([sklearn.clone(clf1)])

    stack = EnsembleStack(cv=3)

    stack.add_layer(layer_1)
    stack.add_layer(layer_2)

    sclf = EnsembleStackClassifier(stack)

    clf_list = [clf1, clf2, clf3, eclf, sclf]
    lbl_list = ['Logistic Regression', 'Random Forest', 'RBF kernel SVM', 'Ensemble', 'Stacking']

    pipe_lrSVC=sclf

    # pipe_lrSVC=SVC(probability=True,class_weight='balanced')
    #svm=LinearSVC(C=10)
    #pipe_lrSVC=CalibratedClassifierCV(svm)
    pipe_lrSVC.fit(np.array(preprocessing.scale(X)),np.array(Y))
    pickle.dump(pipe_lrSVC,open(output_file+'.pickle','wb'))
    print 'SVM trained successfully for event %s!' % (event_name)+" round num %s" % (round_num)
