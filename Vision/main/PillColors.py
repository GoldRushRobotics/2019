import math
import time
import cv2


def findPillarColor(x, y, width, height, image):
    H_Upper = y - height
    H_Lower = y
    W_Upper = x + width
    W_Lower = x

    # img[height_range, width_range]
    cropped = image[W_Lower:W_Upper, H_Upper:H_Lower]

    if cv2.waitKey(25) & 0xFF == ord('q'):
        exit()

    totalPix = (0, 0, 0)

    for h in range(0, height - 1):
        for w in range(0, width - 1):
            totalPix = totalPix + cropped[w][h]

    avgPix = totalPix / ((width) * (height))

    # print(avgPix)

    colors = {"b": (255, 0, 0),
              "g": (0, 255, 0),
              "r": (0, 0, 255),
              "y": (0, 180, 255)
              }

    manhattan = lambda x, y: abs(x[0] - y[0]) + \
                             abs(x[1] - y[1]) + abs(x[2] - y[2])
    distances = {k: manhattan(v, avgPix) for k, v in colors.items()}
    color = min(distances, key=distances.get)
    #print(color)

    return color 


