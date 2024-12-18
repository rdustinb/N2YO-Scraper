from support import restapi, dataHandling, debug
import requests
import json

# Debug Levels
__DEBUG_0   = 0
__DEBUG_V   = 1
__DEBUG_VV  = 2
__DEBUG_VVV = 3

debug.setDebugLevel(__DEBUG_V)

# Generate the REST API URL
thisRestUrl = restapi.buildUrl(25338)
debug.debugPrint("The Radio Passes URL is set as:", __DEBUG_V)
debug.debugPrint("%s"%thisRestUrl, __DEBUG_V)

## Create the request and capture the JSON response
#response = requests.get(thisRestUrl)
#jsonData = response.json()
#debug.debugPrint(jsonData, __DEBUG_VVV)
#
## Write the JSON to a file for future use
#dataHandling.setLocalData(localDataFolder="localData", localDataFilename="noaa15.json", jsonData=jsonData)

