!/bin/bash
ffmpeg_path=/home/ubuntu/tools/FFmpeg/build/bin/
export PATH=$opensmile_path:$speech_tools_path:$ffmpeg_path:$PATH
opensmile_path=/home/ubuntu/tools/opensmile-2.3.0/bin/linux_x64_standalone_static
export LD_LIBRARY_PATH=$ffmpeg_path/libs:$opensmile_path/lib:$LD_LIBRARY_PATH
video_path=../video
mkdir audio
mkdir mfcc
mkdir temp
# 1. ffmpeg extracts the audio track from each video file into a wav file
size=$(cat "list/all.video" | wc -l)
i=0
for line in $(cat "list/all.video"); do
#for line in HVC1012; do 
	if [ ! -f audio/${line}.wav  ]; then
        i=$((i+1))
	echo $i / $size ${line} 
	ffmpeg -y -i $video_path/${line}.mp4 -f wav temp/tmp.wav
	#ffmpeg -y -i $video_path/${line}.mp4 -ac 1 -f wav audio/${iline}.wav
	#ch_wave temp/tmp.wav -c 0 -o audio/$line.wav
        sox temp/tmp.wav -c 1 audio/${line}.wav
        rm -rf temp/tmp.wav
fi
done



