import threading
'''
This file is to house all multithreading implimentation used
'''


class threadedFind(threading.Thread):

    def __init__(self, threadID, name, finder, color, goHome=False):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.goHome = goHome
        self.color = color
        self.finder = finder
        self._return = None

    def run(self):
        print(self.threadID, self.name)
        if self.goHome:

            self._return = self.finder.findPill(goHome)

        else:
            self._return = self.finder.findColored(color)

    def getVals(self):
        return self._return
