from sklearn.calibration import CalibratedClassifierCV
from sklearn import preprocessing
import commands
import numpy as np
import os
from sklearn.svm.classes import SVC
from sklearn.svm import LinearSVC
import cPickle
import sys
import pickle
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score


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

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print "Usage: {0} model_file feat_dir event_name".format(sys.argv[0])
        print "event_name P001/2/3"
        print "feat_dir -- dir of feature files"
        print "model_file reads from the svm model train_file_P00X_Xround_imtraj/SIFT/CNN"
        exit(1)

    model_file = sys.argv[1]
    feat_dir = sys.argv[2]
    event_name=sys.argv[3]
    pipe_lrSVC=pickle.load(open(model_file+'.pickle','rb'))

    test_list="list/test.video"
    X=np.asarray([])
    count=0
    for line in open(test_list,"r"):
        count=count+1
    #    if count%100==0:
     #       print count
        audio_name=line.split(" ")[0].strip()
        if "imtraj" in feat_dir: 
            feat_vec=import_imtraj_txt(feat_dir+audio_name+".spbof")
        else:
            feat_vec=np.genfromtxt(feat_dir+audio_name,delimiter=";")
        if len(X)==0:
            X=[feat_vec]
        else:
            X=np.append(X,[feat_vec],axis=0)
    Y=pipe_lrSVC.predict_proba(preprocessing.scale(X))


    fclassification_write=open("classification_results/"+event_name+"_class.txt","w")
    Y_discrete=pipe_lrSVC.predict(preprocessing.scale(X))
    for i in range(len(Y_discrete)):
        fclassification_write.write(str(Y_discrete[i])+"\n")
    fclassification_write.close()
    fwrite=open("score_results/"+event_name+"_score.txt","w")
    for i in range(len(Y)):
        fwrite.write(str(Y[i][1])+"\n")
    fwrite.close()
