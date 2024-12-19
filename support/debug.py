
class DebugClass:
    def __init__(self, thisDebugLevel=0):
        self.__THISDEBUG = thisDebugLevel
    
    def setDebugLevel(self, newDebugLevel):
        self.__THISDEBUG = newDebugLevel
    
    def debugPrint(self, thisStatement, debugThreshold=0):
        if self.__THISDEBUG >= debugThreshold:
            print(thisStatement)
