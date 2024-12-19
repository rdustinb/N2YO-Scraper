from support import restapi, dataHandling, debug
import requests
import json

# Debug Levels
__DEBUG_0   = 0
__DEBUG_V   = 1
__DEBUG_VV  = 2
__DEBUG_VVV = 3

debug.setDebugLevel(__DEBUG_V)

# Initialize the restapi instance
thisRestApi = restapi.RestApiClass()

## Create the request and capture the JSON response
#response = requests.get(thisRestUrl)
#jsonData = response.json()
#debug.debugPrint(jsonData, __DEBUG_VVV)
#
## Write the JSON to a file for future use
#dataHandling.setLocalData(localDataFolder="localData", localDataFilename="noaa15.json", jsonData=jsonData)

