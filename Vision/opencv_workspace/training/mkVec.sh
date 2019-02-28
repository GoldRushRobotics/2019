#!/bin/bash
#PBS -N opencv2Train
#PBS -q copperhead
#PBS -d /users/gbrown57/
#PBS -l walltime=00:15:00
#PBS -l nodes=1:ppn=2
#PBS -l mem=8GB

cd opencv

for type in BallPos CubePos TelsPos; do
  for f in ./$type/*.png; do
    echo $f
    #opencv_createsamples -img "$f" -bg bg.txt -info info/info"$f".lst -pngoutput info -maxxangle 1 -maxyangle .5 -maxzangle 0.5 -num 4096;
    #mkdir "$type"/vecs/
    #opencv_createsamples -info info/info"$f".lst -num 4096 -w 32 -h 32 -vec "$type"/vecs/positives"$f".vec
  done
done

python mergevec.py -v "$1"/vecs/positives./"$1"/ -o "$1"/finalVec.vec

