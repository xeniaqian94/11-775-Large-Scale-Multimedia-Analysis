#!/bin/bash
ffmpeg_path=/home/ubuntu/tools/FFmpeg/build/bin/
export PATH=$opensmile_path:$speech_tools_path:$ffmpeg_path:$PATH
export LD_LIBRARY_PATH=$ffmpeg_path/libs:$opensmile_path/lib:$LD_LIBRARY_PATH

video_path=../video   # path to the directory containing all the videos. In this example setup, we are linking all the videos to "../video"

video_output_path=../video_cutted

#cat train_dev.video test.video > all.video


count=0
for line in $(cat "list/all.video"); do
    if [ ! -f $video_output_path/${line}.mp4  ]; then 
    echo $count ${line}
    count=$((count+1))
    ffmpeg -y -ss 0 -i $video_path/$line.mp4 -strict experimental -t 10 -r 15 -vf scale=320x240,setdar=4:3 $video_output_path/$line.mp4 
fi;
done
