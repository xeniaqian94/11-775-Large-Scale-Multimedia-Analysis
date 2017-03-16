opensmile_path=/home/ubuntu/tools/openSMILE-2.1.0/bin/linux_x64_standalone_static
speech_tools_path=/home/ubuntu/tools/speech_tools/bin
ffmpeg_path=/home/ubuntu/tools/ffmpeg-2.2.4
map_path=./mAP
export PATH=$opensmile_path:$speech_tools_path:$ffmpeg_path:$map_path:$PATH
export LD_LIBRARY_PATH=$ffmpeg_path/libs:$opensmile_path/lib:$LD_LIBRARY_PATH


echo "#####################################"
echo "#       MED with ASR Features       #"
echo "#####################################"
mkdir -p asr_pred
# iterate over the events
feat_dim_asr=500
feature_name="tf"
#feature_name="tfidf"
method="asroutput_tedlium_complete"

for event in P001 P002 P003; do
  echo "=========  Event $event  ========="
  # now train a svm model
  python scripts/train_svm.py $event $method"_"$feat_dim_asr"_"$feature_name/ $feat_dim_asr asr_pred/svm.$event.$feat_dim_asr.model || exit 1;
  # apply the svm model to *ALL* the testing videos;
  # output the score of each testing video to a file ${event}_pred 
  python scripts/test_svm.py asr_pred/svm.$event.$feat_dim_asr.model $method"_"$feat_dim_asr"_"$feature_name/ $feat_dim_asr asr_pred/${event}_${feat_dim_asr}_pred || exit 1;
  # compute the average precision by calling the mAP package
  #ap list/${event}_test_label asr_pred/${event}_${feat_dim_asr}_pred
done
