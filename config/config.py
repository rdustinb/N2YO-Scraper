from config import myconfig

# Information about the N2YO API Requests:
#       https://www.n2yo.com/api/

__apiKeyFlag = "&apiKey=%s"%(myconfig.myKey)
__baseUrl = "https://api.n2yo.com/rest/v1/satellite"

# NORAD IDs can be looked up here:
#       https://www.n2yo.com/database/
NOAA15ID = 25338
NOAA18ID = 28654
NOAA19ID = 33591
NOAA20ID = 43013

# Initialize some internal vars
__thisPredictionDaySpan = 10
__thisMinimumApparentElevation = 45
__thisNoradId = NOAA20ID
__thisUrl = ""

def setPredictionDaySpan(thisPredictionDaySpan):
    global __thisPredictionDaySpan
    __thisPredictionDaySpan = thisPredictionDaySpan

def setMinimumApparentElevation(thisMinimumApparentElevation):
    global __thisMinimumApparentElevation
    __thisMinimumApparentElevation = thisMinimumApparentElevation

def setNoradId(thisNoradId):
    global __thisNoradId
    __thisNoradId = thisNoradId

def buildUrl():
    # This sets the URL string globally for later referencing if needed...
    global __thisUrl
    __thisUrl = "%s/radiopasses/%s/%s/%s/%s/%s/%s/%s"%(
        str(__baseUrl),
        str(__thisNoradId),
        str(myconfig.myLatitude),
        str(myconfig.myLongitude),
        str(myconfig.myAltitudeMeters),
        str(__thisPredictionDaySpan),
        str(__thisMinimumApparentElevation),
        str(__apiKeyFlag)
    )

    # Return the URL string
    return __thisUrl
