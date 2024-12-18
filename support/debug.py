
__THISDEBUG = 0

def setDebugLevel(newDebugLevel):
    global __THISDEBUG
    __THISDEBUG = newDebugLevel

def debugPrint(thisStatement, debugThreshold=0):
    global __THISDEBUG

    if __THISDEBUG >= debugThreshold:
        print(thisStatement)
