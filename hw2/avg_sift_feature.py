
import cv2
import numpy as np
import sys
from keras.preprocessing import image
from keras.applications import vgg16
from keras.models import Model
import numpy as np
import os.path
# I cropped out each stereo image into its own file.
# You'll have to download the images to run this for yourself
inputDir=sys.argv[1]  #../keras/
allList=sys.argv[2]
outputDir=sys.argv[3]      #../avg_keras/

with open(allList,"r") as videoListFile:
    videoNameList=[name.strip() for name in videoListFile.readlines() if len(name)>0]
#videoNameList=np.genfromtxt(allList)
print len(videoNameList)
print videoNameList
count=0
for videoName in videoNameList:
  if not os.path.exists(outputDir+videoName):
     filePath=inputDir+videoName
     vectors=np.genfromtxt(filePath,delimiter=";")
     if not vectors is None:
        vector=sum(vectors)/len(vectors)
        with open(outputDir+videoName,"a") as f_handle:
           np.savetxt(f_handle,vector,delimiter=';') 
