from keras.preprocessing import image
from keras.layers import Conv2D, MaxPooling2D, Flatten
from keras.layers import Input, LSTM, Embedding, Dense
from keras.models import Model, Sequential
from keras.models import load_model
from keras.losses import categorical_crossentropy
from keras.optimizers import SGD
from sklearn.model_selection import train_test_split
import cv2
import random
import sys
import os
import numpy as np
import tensorflow as tf
image_ordering_dim = "tf"


def split_hold(imgs, locs, trainPer):
    random = 42
    imgs, X_test, locs, Y_test = train_test_split(
        imgs, locs, test_size=1 - trainPer, random_state=random)
    X_train, X_holdout, Y_train, Y_holdout = train_test_split(
        imgs, locs, test_size=1 - trainPer, random_state=random)

    return (X_train, X_test, X_holdout, Y_train, Y_test, Y_holdout)


def validate_holdout(model, holdout, target):
    predictions = model.predict(holdout, batch_size=128, verbose=1)
    score = tf.losses.log_loss(target, predictions)
    return score


def trainModel(data, sh):

    (X_train, X_test, X_holdout, Y_train, Y_test, Y_holdout) = data

    model = Sequential()
    model.add(Conv2D(64, 20, border_mode='valid', input_shape=sh))
    model.add(Conv2D(64, 15, activation='relu'))
    model.add(MaxPooling2D(pool_size=(3, 3), padding='same'))
    model.add(Conv2D(128, 10, activation='relu', padding='same'))
    model.add(Conv2D(128, 10, activation='relu', padding='same'))  # error
    model.add(MaxPooling2D(pool_size=(3, 3), padding='same'))
    model.add(Conv2D(256, 5, activation='relu', padding='same'))
    model.add(Conv2D(256, 5, activation='relu', padding='same'))
    model.add(Conv2D(256, 5, activation='relu', padding='same'))
    model.add(MaxPooling2D(pool_size=(3, 3), padding='same'))
    model.add(Flatten())

    model.add(Dense(5))

    model.compile(loss=categorical_crossentropy,
                  optimizer=SGD(lr=0.01, momentum=0.9, nesterov=True))

    model.fit(X_train, Y_train, batch_size=64, nb_epoch=10,
              verbose=1, validation_data=(X_test, Y_test))

    score = model.evaluate(X_test, Y_test, verbose=0)

    holdScore = validate_holdout(model, X_holdout, Y_holdout)

    return model, score, holdScore


def loadImages(inFile, trainPer=.8):
    datagen = image.ImageDataGenerator(rescale=1. / 255)
    # file = os.listdir(inPath)
    sh = (64, 36)
    # print(files)

    # 49991_0073_0052_0077_0077.jpg,1,73,52,77,77

    imgs = np.empty([0, 64, 36, 1])
    locs = np.empty([5, 0])

    f = open(inFile, "r")
    lines = f.readlines()
    f.close()
    points = 0
    random.shuffle(lines)

    for line in lines:
        ls = line.split(",")
        # print(ls[0])
        img = image.load_img(ls[0], target_size=(64, 36), grayscale=True)

        # img = cv2.imread(ls[0], cv2.IMREAD_GRAYSCALE)

        arr = image.img_to_array(img)
        arr = np.expand_dims(arr, axis=0)

        loc = np.array([
            [int(ls[1]) / 4],
            [int(ls[2]) / sh[0]],
            [int(ls[3]) / sh[1]],
            [int(ls[4]) / sh[0]],
            [int(ls[5]) / sh[1]]
        ])

        imgs = np.append(imgs, arr, axis=0)
        locs = np.append(locs, loc, axis=1)

        if points > 10:
            break
        else:
            points += 1

    locs = np.transpose(locs)

    data = split_hold(
        imgs, locs, trainPer)

    return data, (sh[0], sh[1], 1)

if __name__ == '__main__':

    inPath = sys.argv[1]
    try:
        trainPer = sys.argv[2]
        data, shape = loadImages(inPath, trainPer)
    except:
        data, shape = loadImages(inPath)

    # print(train)
    model, score, holdScore = trainModel(data, shape)

    print("Score from test data: {0}".format(score))
    print("Score from holdout data: {0}".format(holdScore))

    print("Saving model")
    model.save('objDetection.h5')
