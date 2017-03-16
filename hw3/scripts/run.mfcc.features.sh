!/bin/bash
ffmpeg_path=/home/ubuntu/tools/FFmpeg/build/bin/
export PATH=$opensmile_path:$speech_tools_path:$ffmpeg_path:$PATH
opensmile_path=/home/ubuntu/tools/opensmile-2.0-rc1/opensmile/
export LD_LIBRARY_PATH=$ffmpeg_path/libs:$opensmile_path/lib:$LD_LIBRARY_PATH
size=$(cat "list/all.video" | wc -l)
i=0
for line in $(cat "list/all.video"); do
if [ ! -f mfcc/$line.mfcc.csv  ]; then

	i=$((i+1))
	echo $i / $size ${line} 
        SMILExtract -C config/MFCC12_0_D_A.conf -I audio/$line.wav -O mfcc/$line.mfcc.csv
fi;
done



