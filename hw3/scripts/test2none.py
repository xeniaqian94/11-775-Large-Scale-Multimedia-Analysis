import numpy as np
import sys
# import shutil
# from keras.preprocessing import image
# from keras.applications import vgg16
# from keras.models import Model
import numpy as np
import os.path
import shutil
#inputDirs=sys.argv[1]  #../keras/
allList=sys.argv[1]
outputDir=sys.argv[2]

with open(allList,"r") as videoListFile:
        videoNameList=[name.strip() for name in videoListFile.readlines() if len(name)>0]
#videoNameList=np.genfromtxt(allList)
print len(videoNameList)
#print videoNameList

for videoName in videoNameList:
        if os.path.exists(outputDir+videoName+".txt"):
                shutil.copy2(outputDir+videoName+".txt",outputDir+videoName)
