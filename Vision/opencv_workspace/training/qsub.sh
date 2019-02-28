#!/bin/bash
#PBS -q copperhead
#PBS -d /users/gbrown57/opencv
#PBS -l walltime=16:00:00
#PBS -l nodes=6:ppn=2
#PBS -l mem=16GB

opencv_traincascade -data $out -vec $vec -bg $bg -numPos 4000 -numNeg 2000 -numStages 6 -w 32 -h 32 -precalcValBufSize 4096 -precalcIdxBufSize 4096 -bt LB
