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

iframeDir=sys.argv[1]  #../keyframe/
allList=sys.argv[2]
numFrame=int(sys.argv[3])  #25
outputDir=sys.argv[4]      #../keras/

with open(allList,"r") as videoListFile:
    videoNameList=[name.strip() for name in videoListFile.readlines() if len(name)>0]
#videoNameList=np.genfromtxt(allList)
print len(videoNameList)
print videoNameList
base_model = vgg16.VGG16(weights='imagenet')
model = Model(input=base_model.input, output=base_model.get_layer('fc2').output)
count=0
for videoName in videoNameList:
  if not os.path.exists(outputDir+videoName):
     for frameId in range(1,numFrame+1):
        count=count+1
        print count,videoName, frameId
        img_path=iframeDir+iframeDir.split("/")[1]+"_"+videoName+'%09d'%frameId+".jpg"

        if os.path.isfile(img_path):
           img = image.load_img(img_path, target_size=(224, 224))
           if not img is None:
              x = image.img_to_array(img)
              Xs = np.expand_dims(x, axis=0)
              Xs = vgg16.preprocess_input(Xs)
              features = model.predict(Xs)
              if not features is None:
                 with open(outputDir+videoName,"a") as f_handle:
                    np.savetxt(f_handle,features,delimiter=';')
