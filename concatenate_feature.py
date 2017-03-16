# import cv2
import numpy as np
import sys
# import shutil
# from keras.preprocessing import image
# from keras.applications import vgg16
# from keras.models import Model
import numpy as np
import os.path

inputDirs=sys.argv[1].split(":")  #../keras/
allList=sys.argv[2]
outputDir=sys.argv[3]      #../avg_keras/

feature_length=dict()
feature_length["keras"]=4096
feature_length["mfcc"]=200

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
				if key in filePath:
					dimension=feature_length[key]
			if (os.path.exists(filePath)):
				vector=np.genfromtxt(filePath,delimiter=";")
			 
			 # print len(vector),dimension
				if len(vector)==dimension:
					concatenated=concatenated+list(vector)
				else:
					print videoName,str(len(vector)),str(dimension)
			else:    
				concatenated+=list(np.zeros(dimension))
 
		with open(outputDir+videoName,"a") as f_handle:
			np.savetxt(f_handle,np.asarray(concatenated),delimiter=';')

