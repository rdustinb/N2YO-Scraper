import configparser

class RestApiClass:
    ################################
    # Global Variables
    __myKey             = ""
    __myLatitude        = ""
    __myLongitude       = ""
    __myAltitudeMeters  = ""
    __myThresholdAngle  = ""
    __myPredictionDays  = ""
    __myNoradIds        = list()
    __apiKeyFlag        = ""
    __baseUrl           = ""
    __myUrls            = dict()
    
    ################################
    # Initialize from the config.ini file
    def __init__(self):
        print("__init__()")
        ################################
        # Get the configuration
        # Create a config parser object
        config = configparser.ConfigParser()
        
        # Read the configuration file (this just needs to be relative to the top executable)
        config.read('config.ini')
        
        # Access values from the configuration file
        self.__myKey             = config.get('restapi', 'myKey')
        self.__myLatitude        = config.get('restapi', 'myLatitude')
        self.__myLongitude       = config.get('restapi', 'myLongitude')
        self.__myAltitudeMeters  = config.get('restapi', 'myAltitudeMeters')
        self.__myThresholdAngle  = config.get('restapi', 'myThresholdAngle')
        self.__myPredictionDays  = config.get('restapi', 'myPredictionDays')
        # NORAD IDs can be looked up here:
        #       https://www.n2yo.com/database/
        self.__myNoradIds        = config.get('satellites', 'myNoradIds').split()
        
        ################################
        # Information about the N2YO API Requests:
        #       https://www.n2yo.com/api/
        self.__apiKeyFlag        = "&apiKey=%s"%(self.__myKey)
        self.__baseUrl           = "https://api.n2yo.com/rest/v1/satellite"

        ################################
        # Loop through all the NORAD IDs Defined by the user
        for thisNoradId in self.__myNoradIds:
            print(thisNoradId)
            self.buildUrl(thisNoradId)
    
    ################################
    # Top Functions
    def buildUrl(self,thisNoradId):
        print("buildUrl()")
    
        self.__myUrls[thisNoradId] = "%s/radiopasses/%s/%s/%s/%s/%s/%s/%s"%(
            str(self.__baseUrl),
            str(thisNoradId),
            str(self.__myLatitude),
            str(self.__myLongitude),
            str(self.__myAltitudeMeters),
            str(self.__myPredictionDays),
            str(self.__myThresholdAngle),
            str(self.__apiKeyFlag)
        )

        print(self.__myUrls[thisNoradId])
