!/bin/bash
ffmpeg_path=/home/ubuntu/tools/FFmpeg/build/bin/
opensmile_path=/home/ubuntu/tools/opensmile-2.3.0/bin/linux_x64_standalone_static
export PATH=$opensmile_path:$speech_tools_path:$ffmpeg_path:$PATH
export LD_LIBRARY_PATH=$ffmpeg_path/libs:$opensmile_path/lib:$LD_LIBRARY_PATH
video_path=../video

start=`date +%s`
method=tedlium
mkdir asroutput_$method
cp /home/ubuntu/tools/eesen-transcriber/Makefile.options_$method /home/ubuntu/tools/eesen-transcriber/Makefile.options

for line in $(cat "list/all.video"); do
if [ ! -f asroutput_$method/${line}.txt  ]; then


        i=$((i+1))

        end=`date +%s`

        runtime=$((end-start))
        echo "Progress "$i / $size $line " " $runtime 
        rm -rf ../tools/eesen-offline-transcriber/build/
        mkdir ../tools/eesen-offline-transcriber/build/
        echo $(ls ../tools/eesen-offline-transcriber/build/ | wc -l)
        ##ffmpeg -y -i $video_path/${line}.mp4 -f wav temp/tmp.wav

        ../tools/eesen-offline-transcriber/speech2text.sh --txt asroutput_$method/${line}.txt audio/${line}.wav
fi;
done


