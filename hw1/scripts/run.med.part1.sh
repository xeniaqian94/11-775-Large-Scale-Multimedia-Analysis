
#!/bin/bash

# An example script for multimedia event detection (MED) of Homework 1
# Before running this script, you are supposed to have the features by running run.feature.sh 

# Note that this script gives you the very basic setup. Its configuration is by no means the optimal. 
# This is NOT the only solution by which you approach the problem. We highly encourage you to create
# your own setups. 

# Paths to different tools; 
opensmile_path=/home/ubuntu/tools/openSMILE-2.1.0/bin/linux_x64_standalone_static
speech_tools_path=/home/ubuntu/tools/speech_tools/bin
ffmpeg_path=/home/ubuntu/tools/ffmpeg-2.2.4
map_path=/home/ubuntu/tools/mAP
export PATH=$opensmile_path:$speech_tools_path:$ffmpeg_path:$map_path:$PATH
export LD_LIBRARY_PATH=$ffmpeg_path/libs:$opensmile_path/lib:$LD_LIBRARY_PATH

#echo "#####################################"
#echo "#       MED with MFCC Features      #"
#echo "#####################################"

echo "#####################################"
echo "#       MED with MFCC Features      #"
echo "#####################################"
mkdir -p mfcc_pred
# iterate over the events
feat_dim_mfcc=200 #200?
for event in P001 P002 P003; do
  echo "=========  Event $event  ========="
  # now train a svm model
  #python scripts/train_svm.py $event mfcc_feature_$feat_dim_mfcc/ $feat_dim_mfcc mfcc_pred/svm.$event.model || exit 1;
  # apply the svm model to *ALL* the testing videos;
  # output the score of each testing video to a file ${event}_pred 
  python scripts/test_svm.py mfcc_pred/svm.$event.model mfcc_feature_$feat_dim_mfcc/ $feat_dim_mfcc mfcc_pred/${event}_pred || exit 1;
  # compute the average precision by calling the mAP package
#  ap list/${event}_test_label mfcc_pred/${event}_pred
done

