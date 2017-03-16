ffmpeg_path=/home/ubuntu/tools/ffmpeg-2.2.4
map_path=/home/ubuntu/tools/mAP
export PATH=$opensmile_path:$speech_tools_path:$ffmpeg_path:$map_path:$PATH
export LD_LIBRARY_PATH=$ffmpeg_path/libs:$opensmile_path/lib:$LD_LIBRARY_PATH

echo "#####################################"
echo "#       MED with KERAS Features    #"
echo "#####################################"

for event in P001 P002 P003; do
      echo "Event $event test set prediction"
      python predict_svm.py model/svm.avg_keras.${event}_all.model ../avg_keras/  ${event}   #model_file feat_dir event_name round_num output_file
done





