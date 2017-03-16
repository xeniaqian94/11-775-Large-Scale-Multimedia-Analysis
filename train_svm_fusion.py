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
from sklearn.metrics import accuracy_score
from sklearn.metrics import recall_score
from sklearn.metrics import confusion_matrix
import commands


import itertools

import sklearn

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

from brew.base import Ensemble, EnsembleClassifier
from brew.stacking.stacker import EnsembleStack, EnsembleStackClassifier
from brew.combination.combiner import Combiner

def most_common(X):
    y=np.zeros(X.shape[0])
    for i in range(X.shape[0]):
        y[i]=max(list(X[i]),key=list(X[i]).count)
    # return max(set(lst), key=lst.count)
    return y

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
    feat_names=sys.argv[3].split(":")
    method=sys.argv[4] #AVG or MAX
    output_file = "pred/validation_"+"".join(feat_names)+"_"+event_name+"_"+round_num


    if not round_num=="all":
        rount_num=int(round_num)
        train_list="list/"+event_name+"_train_"+str(round_num)
    else:
      train_list="list/train_dev"


    X=np.zeros((len(open("pred/validation_"+feat_names[0]+"_"+event_name+"_"+round_num,"r").readlines()),len(feat_names)))
    for i in range(len(feat_names)):
        X[:,i]=np.genfromtxt("pred/validation_"+feat_names[i]+"_"+event_name+"_"+round_num,delimiter=";")

    aggregated_X=np.mean(X,axis=1)
    np.savetxt(output_file,aggregated_X)

    Y_truth=[]
    groundtruth_label="list/"+event_name+"_validation_label_"+str(round_num)
    for line in open(groundtruth_label,"r"):
        Y_truth+=[int(line.strip())]

    
    ap_output=commands.getstatusoutput("ap "+groundtruth_label+" "+output_file)

    X_label=np.zeros((len(open("classification/validation_"+feat_names[0]+"_"+event_name+"_"+round_num,"r").readlines()),len(feat_names)))
    for i in range(len(feat_names)):
        X_label[:,i]=np.genfromtxt("classification/validation_"+feat_names[i]+"_"+event_name+"_"+round_num,delimiter=";")


    print X_label.shape
    aggregated_X_label=most_common(X_label)
    output_file = "classification/validation_"+"".join(feat_names)+"_"+event_name+"_"+round_num

    # fwrite=open(output_file,"w")
    # for i in range(len(aggregated_X_label)):
    #     fwrite.write(str(aggregated_X_label[i][1])+"\n")
    # fwrite.close()

    np.savetxt(output_file,aggregated_X_label)

    print event_name+" 3 FOLD ROUND "+str(round_num)+" CROSS VALIDATION RESULT MAP: "+ap_output[1].split(": ")[1]
    print event_name+" 3 FOLD ROUND "+str(round_num)+" CROSS VALIDATION RESULT CLASS ACCURACY: "+str(accuracy_score(Y_truth,aggregated_X_label))
    print event_name+" 3 FOLD ROUND "+str(round_num)+" CROSS VALIDATION RESULT TRUE POSITIVE RATE: "+str(recall_score(Y_truth,aggregated_X_label))
    CM=confusion_matrix(Y_truth,aggregated_X_label)
#    print str(CM[1][1]*1.0/(CM[1][1]+CM[1][0]))
    print event_name+" 3 FOLD ROUND "+str(round_num)+" CROSS VALIDATION RESULT TRUE NEGATIVE RATE: "+str(CM[0][0]*1.0/(CM[0][0]+CM[0][1]))





    # pipe_lrSVC=SVC(probability=True,class_weight='balanced')
    # #svm=LinearSVC(C=10)
    # #pipe_lrSVC=CalibratedClassifierCV(svm)
    # for line in open(groundtruth_label,"r"):
    #     Y_truth+=[int(line.strip())]
    # pipe_lrSVC.fit(preprocessing.scale(X),Y_truth)


    

    # Y=pipe_lrSVC.predict_proba(preprocessing.scale(X))
    # f_write=open(output_file,"w")
    # for i in range(len(Y)):
    #     f_write.write(str(Y[i][1])+"\n")
    # f_write.close()

    # # np.savetxt(output_file,aggregated_X)
    # ap_output=commands.getstatusoutput("ap "+groundtruth_label+" "+output_file)

   

    # print event_name+" 3 FOLD ROUND "+str(round_num)+" CROSS VALIDATION RESULT MAP: "+ap_output[1].split(": ")[1]





    
#     X=np.asarray([])
#     Y=[]
#     pos_count=0
#     neg_count=0
#     count=0
#     print train_list,feat_dir
#     for line in open(train_list,"r"):
#         audio_name=line.split(" ")[0]
#         # print audio_name
#         count=count+1
#  #       if (count%100==0):
# #      print count
#         label=line.split(" ")[1].split("\n")[0]
#         if "imtraj" in feat_dir: 
#             feat_vec=import_imtraj_txt(feat_dir+audio_name+".spbof")
#         else:
#             feat_vec=np.genfromtxt(feat_dir+audio_name,delimiter=";")
#         if (label==event_name):
#             label=1
#             pos_count+=1
#         else:
#             label=0
#             neg_count+=1
#         if len(X)==0:
#             # print feat_vec,np.sum(feat_vec)
#             X=[feat_vec]
#         else:
#             # print feat_vec,np.sum(feat_vec)
#             X=np.append(X,[feat_vec],axis=0)
#         Y=Y+[label]
    
#     print "Data loading finished positive "+str(pos_count)+" negative "+str(neg_count)
#     #pipe_lrSVC=SVC(C=10,gamma=0.0001,probability=True)


#     clf1 = LogisticRegression(random_state=0)
#     clf2 = RandomForestClassifier(random_state=0)
#     clf3 = SVC(random_state=0, probability=True)

#     # Creating Ensemble
#     ensemble = Ensemble([clf1, clf2, clf3])
#     eclf = EnsembleClassifier(ensemble=ensemble, combiner=Combiner('mean'))

#     # Creating Stacking
#     layer_1 = Ensemble([clf1, clf2, clf3])
#     layer_2 = Ensemble([sklearn.clone(clf1)])

#     stack = EnsembleStack(cv=3)

#     stack.add_layer(layer_1)
#     stack.add_layer(layer_2)

#     sclf = EnsembleStackClassifier(stack)

#     clf_list = [clf1, clf2, clf3, eclf, sclf]
#     lbl_list = ['Logistic Regression', 'Random Forest', 'RBF kernel SVM', 'Ensemble', 'Stacking']

#     pipe_lrSVC=sclf

#     # pipe_lrSVC=SVC(probability=True,class_weight='balanced')
#     #svm=LinearSVC(C=10)
#     #pipe_lrSVC=CalibratedClassifierCV(svm)
#     pipe_lrSVC.fit(preprocessing.scale(X),Y)
#     pickle.dump(pipe_lrSVC,open(output_file+'.pickle','wb'))
#     print 'SVM trained successfully for event %s!' % (event_name)+" round num %s" % (round_num)