#!/bin/bash

# An example script for feature extraction of Homework 1

# Note that this script gives you the very basic setup. Its configuration is by no means the optimal. 
# This is NOT the only solution by which you approach the problem. We highly encourage you to create
# your own setups.

# Paths to different tools; 
##opensmile_path=/home/ubuntu/tools/opensmile-2.3.0/bin/linux_x64_standalone_static
##ffmpeg_path=/home/ubuntu/tools/FFmpeg/build/bin/
##export PATH=$opensmile_path:$speech_tools_path:$ffmpeg_path:$PATH
##export LD_LIBRARY_PATH=$ffmpeg_path/libs:$opensmile_path/lib:$LD_LIBRARY_PATH

# Two additional variables
##video_path=../video   # path to the directory containing all the videos. In this example setup, we are linking all the videos to "../video"
##cluster_num=50        # the number of clusters in k-means. Note that 50 is by no means the optimal solution.
                      # You need to explore the best config by yourself.
##mkdir -p audio mfcc kmeans

# This part does feature extraction, it may take quite a while if you have a lot of videos. Totally 3 steps are taken:
# 1. ffmpeg extracts the audio track from each video file into a wav file
# 2. The wav file may contain 2 channels. We always extract the 1st channel using ch_wave
# 3. SMILExtract generates the MFCC features for each wav file
#    The config file MFCC12_0_D_A.conf generates 13-dim MFCCs at each frame, together with the 1st and 2nd deltas. So you 
#    will see each frame totally has 39 dims. 
#    Refer to Section 2.5 of this document http://web.stanford.edu/class/cs224s/hw/openSMILE_manual.pdf for better configuration
#    (e.g., normalization) and other feature types (e.g., PLPs )     
##cat list/train | awk '{print $1}' > list/train.video
##cat list/test | awk '{print $1}' > list/test.video
##cat list/train.video list/test.video > list/all.video
##size=$(cat "list/all.video" | wc -l)
##i=0
##for line in $(cat "list/all.video"); do
##    i=$((i+1))
##    echo $i / $size $line 
##    ffmpeg -y -i $video_path/${line}.mp4 -f wav temp/tmp.wav
##    #ffmpeg -y -i $video_path/${line}.mp4 -ac 1 -f wav audio/$line.wav
##    ##ch_wave temp/tmp.wav -c 0 -o audio/$line.wav
##    sox temp/tmp.wav -c 1 audio/$line.wav
##    SMILExtract -C config/MFCC12_0_D_A.conf -I audio/$line.wav -O mfcc/$line.mfcc.csv
##done
# You may find the number of MFCC files mfcc/*.mfcc.csv is slightly less than the number of the videos. This is because some of the videos
# don't hae the audio track. For example, HVC1221, HVC1222, HVC1261, HVC1794 

# In this part, we train a clustering model to cluster the MFCC vectors. In order to speed up the clustering process, we
# select a small portion of the MFCC vectors. In the following example, we only select 20% randomly from each video. 
##echo "Pooling MFCCs (optional)"
##python scripts/select_frames.py list/train.video 0.2 select.mfcc.csv || exit 1;

# now trains a k-means model using the sklearn package
##echo "Training the k-means model"
##python scripts/train_kmeans.py select.mfcc.csv $cluster_num kmeans.${cluster_num}.model || exit 1;

# Now that we have the k-means model, we can represent a whole video with the histogram of its MFCC vectors over the clusters. 
# Each video is represented by a single vector which has the same dimension as the number of clusters. 
##echo "Creating k-means cluster vectors"
##python scripts/create_kmeans.py kmeans.${cluster_num}.model $cluster_num list/all.video || exit 1;

# Now you can see that you get the bag-of-word representations under kmeans/. Each video is now represented
# by a {cluster_num}-dimensional vector.

# Now we generate the ASR-based features. This requires a vocabulary file to available beforehand. Each video is represented by
# a vector which has the same dimension as the size of the vocabulary. The elements of this vector are the number of occurrences 
# of the corresponding word. The vector is normalized to be like a probability. 
# You can of course explore other better ways, such as TF-IDF, of generating these features.
##echo "Creating ASR features"
#mkdir -p asrfeat
python scripts/create_asrfeat_modified.py list/all.video 983 tfidf|| exit 1;


start=`date +%s`
method=tedlium
mkdir asroutput_$method
cp /home/ubuntu/tools/eesen-transcriber/Makefile.options_$method /home/ubuntu/tools/eesen-transcriber/Makefile.options

for line in $(cat "list/all.video"); do
	i=$((i+1))
    
	end=`date +%s`

	runtime=$((end-start))
	echo "Progress "$i / $size $line " " $runtime 
        rm -rf ../tools/eesen-offline-transcriber/build/*
        mkdir ../tools/eesen-offline-transcriber/build/
        ##ffmpeg -y -i $video_path/${line}.mp4 -f wav temp/tmp.wav
        
	../tools/eesen-offline-transcriber/speech2text.sh --txt asroutput_$method/${line}.txt audio/${line}.wav

done

# Great! We are done!
##echo "SUCCESSFUL COMPLETION"
