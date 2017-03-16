#!/bin/python
import numpy
import os
import cPickle
from sklearn.cluster.k_means_ import KMeans
import sys

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print "Usage: {0}  file_list".format(sys.argv[0])
        #print "vocab_file -- path to the vocabulary file"
        print "file_list -- the list of videos"
        exit(1)

    file_list = sys.argv[1];
    fread = open(file_list,"r")
    for line in fread.readlines():
        mfcc_path = "mfcc/" + line.replace('\n','') + ".mfcc.csv"
        if os.path.exists(mfcc_path) == False:
            continue
        array = numpy.genfromtxt(mfcc_path, delimiter=";")
        numpy.random.shuffle(array)
        select_size = int(array.shape[0] * ratio)
        feat_dim = array.shape[1]



for line in $(cat "list/all.video"); do
    i=$((i+1))
    echo $i / $size $line 
    ffmpeg -y -i $video_path/${line}.mp4 -f wav temp/tmp.wav
    #ffmpeg -y -i $video_path/${line}.mp4 -ac 1 -f wav audio/$line.wav
    ##ch_wave temp/tmp.wav -c 0 -o audio/$line.wav
    sox temp/tmp.wav -c 1 audio/$line.wav
    SMILExtract -C config/MFCC12_0_D_A.conf -I audio/$line.wav -O mfcc/$line.mfcc.csv
done









    print "ASR features generated successfully!"
