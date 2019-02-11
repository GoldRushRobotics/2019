import urllib.request
import cv2
import numpy as np
import os
import subprocess

path = 'cubePos'

def store_raw_images():
    neg_images_link = 'http://www.image-net.org/api/text/imagenet.synset.geturls?wnid=n00523513'
    neg_image_urls = urllib.request.urlopen(neg_images_link).read().decode()
    pic_num = 1

    if not os.path.exists('neg'):
        os.makedirs('neg')

    for i in neg_image_urls.split('\n'):
        try:
            print(i)
            urllib.request.urlretrieve(i, "neg/"+str(pic_num)+".jpg")
            img = cv2.imread("neg/"+str(pic_num)+".jpg",cv2.IMREAD_GRAYSCALE)
            # should be larger than samples / pos pic (so we can place our image on it)
            resized_image = cv2.resize(img, (128, 128))
            cv2.imwrite("neg/"+str(pic_num)+".jpg",resized_image)
            pic_num += 1

        except Exception as e:
            print(str(e))

def create_pos_n_neg():
    for file_type in ['training/courseNeg']:

        for img in os.listdir(file_type):

            if file_type == 'cubePos':
                line = file_type+'/'+img+' 1 0 0 64 64\n'
                with open('training/info/info.dat','a') as f:
                    f.write(line)
            elif file_type == 'training/courseNeg':
                line = file_type+'/'+img+'\n'
                with open('bg.txt','a') as f:
                    f.write(line)
def find_uglies():
    match = False
    for file_type in ['neg']:
        for img in os.listdir(file_type):
            for ugly in os.listdir('uglies'):
                try:
                    current_image_path = str(file_type)+'/'+str(img)
                    ugly = cv2.imread('uglies/'+str(ugly))
                    question = cv2.imread(current_image_path)
                    if ugly.shape == question.shape and not(np.bitwise_xor(ugly,question).any()):
                        print('That is one ugly pic! Deleting!')
                        print(current_image_path)
                        os.remove(current_image_path)
                except Exception as e:
                    print(str(e))
def makePos_samples():
  files = os.listdir("{0}/".format(path))
  for image in files:
    print("{0}/{1}".format(path, image))
    _ = subprocess.call("opencv_createsamples -img {0}/{1} -bg bg.txt -info info/info{1}.lst -pngoutput info -maxxangle 0.5 -maxyangle 0.5 -maxzangle 0.5 -num 776".format(path,image))
    _ = subprocess.call("opencv_createsamples -info info/info{0}.lst -num 776 -w 64 -h 64 -vec positives{0}.vec".format(image))
#makePos_samples()
create_pos_n_neg()

