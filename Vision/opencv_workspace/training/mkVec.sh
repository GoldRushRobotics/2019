


for f in ./$1/*.jpg; do
  opencv_createsamples -img "$f" -bg bg.txt -info info/info"$f".lst -pngoutput info -maxxangle 0.5 -maxyangle 0.5 -maxzangle 0.5 -num 1024;
  mkdir "$1"/vecs/
  opencv_createsamples -info info/info"$f".lst -num 1024 -w 20 -h 20 -vec "$1"/vecs/positives"$f".vec
done

python mergevec.py -v "$1"/vecs/positives./"$1"/ -o "$1"/finalVec.vec

