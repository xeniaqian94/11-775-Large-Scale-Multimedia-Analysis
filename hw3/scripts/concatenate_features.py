# import cv2
import numpy as np
import sys
# import shutil
# from keras.preprocessing import image
# from keras.applications import vgg16
# from keras.models import Model
import numpy as np
import os.path

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

inputDirs=sys.argv[1].split(":")  #../keras/
allList=sys.argv[2]
outputDir=sys.argv[3]      #../avg_keras/

feature_length=dict()
feature_length["keras"]=4096
feature_length["mfcc"]=200
feature_length['imtraj']=32768
feature_length['asr']=2191
with open(allList,"r") as videoListFile:
	videoNameList=[name.strip() for name in videoListFile.readlines() if len(name)>0]
#videoNameList=np.genfromtxt(allList)
print len(videoNameList)
#print videoNameList
count=0
for videoName in videoNameList:
	if not os.path.exists(outputDir+videoName):
		count=count+1
		print count, videoName
		concatenated=list()
		for inputDir in inputDirs:
			filePath=inputDir+videoName
			for key in feature_length.keys():
		#		print key, filePath
				if key in filePath:
					dimension=feature_length[key]
					if (os.path.exists(filePath)):
						if "imtraj" not in filePath:
							vector=np.genfromtxt(filePath,delimiter=";")
						else:
							vector=import_imtraj_txt(filePath)
			 
			 # print len(vector),dimension
						if len(vector)==dimension:
							concatenated=concatenated+list(vector)
						else:
							print videoName,str(len(vector)),str(dimension)
					else:    
						concatenated+=list(np.zeros(dimension))
 
		with open(outputDir+videoName,"w") as f_handle:
			np.savetxt(f_handle,np.asarray(concatenated),delimiter=';')
