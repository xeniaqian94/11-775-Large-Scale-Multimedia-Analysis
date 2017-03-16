#!/bin/bash
ffmpeg_path=/home/ubuntu/tools/FFmpeg/build/bin/
export PATH=$opensmile_path:$speech_tools_path:$ffmpeg_path:$PATH
export LD_LIBRARY_PATH=$ffmpeg_path/libs:$opensmile_path/lib:$LD_LIBRARY_PATH

#video_path=../video   # path to the directory containing all the videos. In this example setup, we are linking all the videos to "../video"


#cat train_dev.video test.video > all.video

count=0
for line in $(cat "list/all.video"); do
    echo $count ${line}
    count=$((count+1))
    #if (( $count % 20 == 0 )) 
    #then 
      #  break
    #fi
    python extract_sift_feature.py ../keyframe/ ${line} 25 ../sift/



done



