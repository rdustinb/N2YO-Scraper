from support import Debug, dataHandling
import configparser, requests, json

class RestApiClass:
    ################################
    # Initialize from the config.ini file
    def __init__(self, thisDebugLevel=0):
        ################################
        # Initialize the Debug instance
        self.__myDebug = Debug.DebugClass(thisDebugLevel)

        self.__myDebug.debugPrint("__init__()", 1)

        ################################
        # Get the configuration
        # Create a config parser object
        config = configparser.ConfigParser()
        
        # Read the configuration file (this just needs to be relative to the top executable)
        config.read('config.ini')
        
        # Access values from the configuration file
        self.__myKey                = config.get('restapi', 'myKey')
        self.__myLatitude           = config.get('restapi', 'myLatitude')
        self.__myLongitude          = config.get('restapi', 'myLongitude')
        self.__myAltitudeMeters     = config.get('restapi', 'myAltitudeMeters')
        self.__myThresholdAngle     = config.get('restapi', 'myThresholdAngle')
        self.__myPredictionDays     = config.get('restapi', 'myPredictionDays')
        # NORAD IDs can be looked up here:
        #       https://www.n2yo.com/database/
        self.__mySatelliteNoradIds  = config.get('satellites', 'mySatelliteNoradIds').split()
        self.__mySatelliteNames     = config.get('satellites', 'mySatelliteNames').split()
        
        ################################
        # Information about the N2YO API Requests:
        #       https://www.n2yo.com/api/
        self.__apiKeyFlag           = "&apiKey=%s"%(self.__myKey)
        self.__baseUrl              = "https://api.n2yo.com/rest/v1/satellite"

        ################################
        # Loop through all the NORAD IDs Defined by the user
        self.__mySatelliteData      = dict()
        for thisNoradId, thisName in zip(self.__mySatelliteNoradIds, self.__mySatelliteNames):
            self.__mySatelliteData[thisNoradId] = list()
            self.__mySatelliteData[thisNoradId].append(thisName)
            self.buildUrl(thisNoradId)
    
    ################################
    # Top Functions
    def buildUrl(self,thisNoradId):
        self.__myDebug.debugPrint("buildUrl()", 1)
    
        self.__mySatelliteData[thisNoradId].append("%s/radiopasses/%s/%s/%s/%s/%s/%s/%s"%(
            str(self.__baseUrl),
            str(thisNoradId),
            str(self.__myLatitude),
            str(self.__myLongitude),
            str(self.__myAltitudeMeters),
            str(self.__myPredictionDays),
            str(self.__myThresholdAngle),
            str(self.__apiKeyFlag)
        ))

        self.__myDebug.debugPrint(thisNoradId, 1)
        self.__myDebug.debugPrint(self.__mySatelliteData[thisNoradId][0], 1)
        self.__myDebug.debugPrint(self.__mySatelliteData[thisNoradId][1], 1)

    # Fetch the JSON Data
    def fetchAllJson(self):
        self.__myDebug.debugPrint("fetchAllJson()", 1)

        # Lookup by NORAD ID
        for thisNoradId in self.__mySatelliteData:
            thisUrl = self.__mySatelliteData[thisNoradId][1]
            thisName = self.__mySatelliteData[thisNoradId][0]
            thisFilename = "%s_%s.json"%(thisNoradId, thisName)
            # Branch based on debug setting
            if(self.__myDebug.getDebugLevel() == 0):
                response = requests.get(thisUrl)
                self.__mySatelliteData[thisNoradId].append(response.json())
                dataHandling.setLocalData("./localData", thisFilename, self.__mySatelliteData[thisNoradId][2])
            else:
                self.__myDebug.debugPrint("Fetching from URL: %s"%(thisUrl), 1)
                self.__myDebug.debugPrint("Storing JSON in: self.__mySatelliteData[%s][3]"%(thisNoradId), 1)
                self.__myDebug.debugPrint("Writing JSON to: %s"%(thisFilename), 1)

