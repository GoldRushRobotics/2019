#!/bin/bash
#PBS -N opencv2Train
#PBS -q copperhead
#PBS -d /users/gbrown57/
#PBS -l walltime=8:00:00
#PBS -l nodes=6:ppn=2
#PBS -l mem=8GB

bg=/users/gbrown57/opencv/bg.txt
vec=/users/gbrown57/opencv/positives./cubePos.vec

cd opencv
pwd
opencv_traincascade -data data -vec $vec -bg $bg -numPos 200 -numNeg 100 -numStages 10 -w 64 -h 64
