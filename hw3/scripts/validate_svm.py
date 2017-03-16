from sklearn.metrics import roc_curve
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
from sklearn.metrics import recall_score
from sklearn.metrics import confusion_matrix
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
    if len(sys.argv) != 6:
        print "Usage: {0} model_file feat_dir event_name round_num output_file".format(sys.argv[0])
        print "output_file path to save the prediction score"
        print "event_name P001/2/3"
        print "round_num 0,1,2?"
        print "feat_dir -- dir of feature files"
        print "model_file reads from the svm model train_file_P00X_Xround_imtraj/SIFT/CNN"
        exit(1)

    model_file = sys.argv[1]
    feat_dir = sys.argv[2]
    event_name=sys.argv[3]
    round_num = int(sys.argv[4])
    output_file = sys.argv[5]
    pipe_lrSVC=pickle.load(open(model_file+'.pickle','rb'))

    test_list="list/"+event_name+"_validation_"+str(round_num)
    X=np.asarray([])
    count=0
    for line in open(test_list,"r"):
        count=count+1
 #       if count%100==0:
#            print count
        audio_name=line.split(" ")[0]
        label=line.split(" ")[1].split("\n")[0]
        if "imtraj" in feat_dir: 
            feat_vec=import_imtraj_txt(feat_dir+audio_name+".spbof")
        else:
            feat_vec=np.genfromtxt(feat_dir+audio_name,delimiter=";")
        if len(X)==0:
            X=[feat_vec]
        else:
            X=np.append(X,[feat_vec],axis=0)
    Y=pipe_lrSVC.predict_proba(preprocessing.scale(X))

    groundtruth_label="list/"+event_name+"_validation_label_"+str(round_num)
    Y_truth=[]

    for line in open(groundtruth_label,"r"):
        Y_truth+=[int(line.strip())]
    fclassification_write=open(output_file.replace("pred/","classification/"),"w")
    Y_discrete=pipe_lrSVC.predict(preprocessing.scale(X))
    #print Y_discrete
    #Y_discrete=[1 if y[1]>y[0] else 0 for y in Y_discrete]
    for i in range(len(Y_discrete)):
        fclassification_write.write(str(Y_discrete[i])+"\n")
    fclassification_write.close()
    fwrite=open(output_file,"w")
    for i in range(len(Y)):
        fwrite.write(str(Y[i][1])+"\n")
    fwrite.close()
    ap_output=commands.getstatusoutput("ap "+groundtruth_label+" "+output_file)

    print model_file.split(".")[1]+" 3 FOLD ROUND "+str(round_num)+" CROSS VALIDATION RESULT MAP: "+ap_output[1].split(": ")[1]
    print model_file.split(".")[1]+" 3 FOLD ROUND "+str(round_num)+" CROSS VALIDATION RESULT CLASS ACCURACY: "+str(accuracy_score(Y_truth,Y_discrete))
    print model_file.split(".")[1]+" 3 FOLD ROUND "+str(round_num)+" CROSS VALIDATION RESULT TRUE POSITIVE RATE: "+str(recall_score(Y_truth,Y_discrete))
    CM=confusion_matrix(Y_truth,Y_discrete)
#    print str(CM[1][1]*1.0/(CM[1][1]+CM[1][0]))
    print model_file.split(".")[1]+" 3 FOLD ROUND "+str(round_num)+" CROSS VALIDATION RESULT TRUE NEGATIVE RATE: "+str(CM[0][0]*1.0/(CM[0][0]+CM[0][1]))
