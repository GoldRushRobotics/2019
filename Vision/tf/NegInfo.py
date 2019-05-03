import sys
import os


def loadImages(inPath):
    "files = os.listdir(inPath)"

    # 49991_0073_0052_0077_0077.jpg 1 73 52 77

    outFile = open("neginfo.lst", "w")

    for file in files:
        # print(file)
        outFile.write("negs/{0},0,0,0,0,0\n".format(file))

    outFile.close()


if __name__ == '__main__':
    inPath = sys.argv[1]
    loadImages(inPath)
