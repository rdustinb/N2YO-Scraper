import configparser

################################
# Global Variables
__myKey             = ""
__myLatitude        = ""
__myLongitude       = ""
__myAltitudeMeters  = ""
__myThresholdAngle  = ""
__myPredictionDays  = ""
__mySatellites      = list()
__apiKeyFlag        = ""
__baseUrl           = ""

################################
# Base Functions
def setPredictionDaySpan(thisPredictionDaySpan):
    global __thisPredictionDaySpan
    __thisPredictionDaySpan = thisPredictionDaySpan

def setMinimumApparentElevation(thisMinimumApparentElevation):
    global __thisMinimumApparentElevation
    __thisMinimumApparentElevation = thisMinimumApparentElevation

def setNoradId(thisNoradId):
    global __thisNoradId
    __thisNoradId = thisNoradId

################################
# Read the Config from the User
def readConfig():
    global __myKey
    global __myLatitude
    global __myLongitude
    global __myAltitudeMeters
    global __myThresholdAngle
    global __myPredictionDays
    global __mySatellites
    global __apiKeyFlag
    global __baseUrl

    ################################
    # Get the configuration
    # Create a config parser object
    config = configparser.ConfigParser()
    
    # Read the configuration file (this just needs to be relative to the top executable)
    config.read('config.ini')
    
    # Access values from the configuration file
    __myKey             = config.get('restapi', 'myKey')
    __myLatitude        = config.get('restapi', 'myLatitude')
    __myLongitude       = config.get('restapi', 'myLongitude')
    __myAltitudeMeters  = config.get('restapi', 'myAltitudeMeters')
    __myThresholdAngle  = config.get('restapi', 'myThresholdAngle')
    __myPredictionDays  = config.get('restapi', 'myPredictionDays')
    # NORAD IDs can be looked up here:
    #       https://www.n2yo.com/database/
    __mySatellites      = config.get('satellites', 'mySatellites').split()
    
    ################################
    # Information about the N2YO API Requests:
    #       https://www.n2yo.com/api/
    __apiKeyFlag        = "&apiKey=%s"%(__myKey)
    __baseUrl           = "https://api.n2yo.com/rest/v1/satellite"

################################
# Top Functions
def buildUrl(thisNoradId):
    global __baseUrl
    global __myLatitude
    global __myLongitude
    global __myAltitudeMeters
    global __myPredictionDays
    global __myThresholdAngle
    global __apiKeyFlag

    readConfig()

    __thisUrl = "%s/radiopasses/%s/%s/%s/%s/%s/%s/%s"%(
        str(__baseUrl),
        str(thisNoradId),
        str(__myLatitude),
        str(__myLongitude),
        str(__myAltitudeMeters),
        str(__myPredictionDays),
        str(__myThresholdAngle),
        str(__apiKeyFlag)
    )

    # Return the URL string
    return __thisUrl

def buildAllUrls():
    pass
