import threading
'''
This file is to house all multithreading implimentation used
'''


class threadedFind(threading.Thread):

    def __init__(self, threadID, name, gray, finder, color=None):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.gray = gray
        self.color = color
        self.finder = finder
        self._return = None

    def run(self):
        print(self.threadID, self.name)
        if self.threadID == 1:
            self._return = self.finder.findFood(self.gray)
        elif self.threadID == 2:
            self._return = self.finder.findTels(self.gray)
        else:
            self._return = self.finder.findPill(self.gray, self.color)

    def getVals(self):
        return self._return
