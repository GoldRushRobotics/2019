import threading
'''
This file is to house all multithreading implimentation used
'''


class threadedFind(threading.Thread):

    def __init__(self, threadID, name, finder, goHome=False):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.goHome = goHome
        self.finder = finder
        self._return = None

    def run(self):
        print(self.threadID, self.name)
        if self.threadID == 1:
            self._return = self.finder.findFood()
        elif self.threadID == 2:
            self._return = self.finder.findTels()
        else:
            self._return = self.finder.findPill(self.goHome)

    def getVals(self):
        return self._return
