ffmpeg_path=/home/ubuntu/tools/ffmpeg-2.2.4
map_path=/home/ubuntu/tools/mAP
export PATH=$opensmile_path:$speech_tools_path:$ffmpeg_path:$map_path:$PATH
export LD_LIBRARY_PATH=$ffmpeg_path/libs:$opensmile_path/lib:$LD_LIBRARY_PATH
method="mfcc_keras"
echo "#####################################"
echo "#       MED with $method Features    #"
echo "#####################################"

for event in P001; do
   for round_num in 0 1 2; do
      echo "Event $event Round $round_num TO BE AVERAGED!"
      #python -W ignore train_svm.py ${event} ${round_num} ./$method/ model/svm.${method}.${event}_${round_num}.model  #event_name round_num feat_dir output_file
      python -W ignore validate_svm.py model/svm.${method}.${event}_${round_num}.model ./${method}/ ${event} ${round_num} pred/validation_${method}_${event}_${round_num}    #model_file feat_dir event_name round_num output_file
   done
   echo " "
     #python -W ignore train_svm.py ${event} all ./$method/  model/svm.${method}.${event}_all.model  #event_name round_num feat_dir output_file
#     python -W ignore predict_svm.py model/svm.${method}.${event}_all.model ./${method}/ ${event} 

done
