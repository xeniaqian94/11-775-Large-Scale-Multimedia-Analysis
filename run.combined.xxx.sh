q#ffmpeg_path=/home/ubuntu/tools/ffmpeg-2.2.4
map_path=./mAP
export PATH=$opensmile_path:$speech_tools_path:$ffmpeg_path:$map_path:$PATH
export LD_LIBRARY_PATH=$ffmpeg_path/libs:$opensmile_path/lib:$LD_LIBRARY_PATH
method="asroutput_tedlium_complete_10000_tfidf"
echo "#####################################"
echo "#       MED with $method Features    #"
echo "#####################################"

for event in P001 P002 P003; do
   for round_num in 0 1 2; do
      echo "Event $event Round $round_num TO BE AVERAGED!"
  python train_svm_fusion.py ${event} ${round_num} keras:mfcc_feature_200_completed:imtraj AVG
  done
   echo " "
done
