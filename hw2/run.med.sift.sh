ffmpeg_path=/home/ubuntu/tools/ffmpeg-2.2.4
map_path=/home/ubuntu/tools/mAP
export PATH=$opensmile_path:$speech_tools_path:$ffmpeg_path:$map_path:$PATH
export LD_LIBRARY_PATH=$ffmpeg_path/libs:$opensmile_path/lib:$LD_LIBRARY_PATH

echo "#####################################"
echo "#       MED with SIFT Features    #"
echo "#####################################"

for cluster_num in 200 500 1000; do 
for event in P001 P002 P003; do
   for round_num in 0 1 2; do
      echo "Event $event Round $round Cluster_num $cluster_num"
      python train_svm.py ${event} ${round_num} ../sift_feature_${cluster_num}/ model/svm.sift.${event}_${round_num}_${cluster_num}.model  #event_name round_num feat_dir output_file
      python validate_svm.py model/svm.sift.${event}_${round_num}_${cluster_num}.model ../sift_feature_${cluster_num}/ ${event} ${round_num} pred/validation_sift_${event}_${round_num}    #model_file feat_dir event_name round_num output_file
   done
   python train_svm.py ${event} all ../sift_feature_${cluster_num}/ model/svm.sift.${event}_all_${cluster_num}.model
done
done





