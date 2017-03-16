ffmpeg_path=/home/ubuntu/tools/FFmpeg/build/bin/
export PATH=$opensmile_path:$speech_tools_path:$ffmpeg_path:$PATH
export LD_LIBRARY_PATH=$ffmpeg_path/libs:$opensmile_path/lib:$LD_LIBRARY_PATH
video_output_path=../video_cutted

keyframe_image_output_path=../keyframe
mkdir $keyframe_image_output_path
count=0
for line in $(cat "list/all.video"); do

	if [ ! -f $keyframe_image_output_path/keyframe_${line}000000001.jpg  ]; then

    echo $count ${line}
    count=$((count+1))
    ffmpeg -i $video_output_path/$line.mp4  -vf select='eq(pict_type\,I)',setpts='N/(25*TB)' $keyframe_image_output_path/keyframe_$line%09d.jpg

fi;

done

