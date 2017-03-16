#!/bin/bash


MAP=1
START=$(date +%s.%N)

echo MED with MFCC 
sh run.med.part1.sh
sh run.med.part2.sh
END=$(date +%s.%N)
#DIFF=$(echo "$END - $START" | bc)

echo Time extracting feautres: $DIFF
#echo MAP: $MAP
#echo P001 MAP: 0.175214
#echo P002 MAP: 0.188034
#echo P003 MAP: 0.209402


#echo P001 CLASS ACCURACY: 0.82905982906
#echo P002 CLASS ACCURACY: 0.811965811966
#echo P003 CLASS ACCURACY: 0.790598290598

#sh run.med.part2.sh

END=$(date +%s.%N)
#DIFF=$(echo "$END - $START" | bc)

echo Time extracting feautres: $DIFF
#echo MAP: $MAP

#echo P001 MAP: $MAPP001
#echo P002 MAP: $MAPP002
#echo P003 MAP: $MAPP003


#echo P001 CLASS ACCURACY: $CAP001
#echo P002 CLASS ACCURACY: $CAP002
#echo P003 CLASS ACCURACY: $CAP003
