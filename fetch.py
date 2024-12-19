from support import RestAPI, dataHandling, Debug
import requests
import json

# Initialize the restapi instance
thisRestApi = RestAPI.RestApiClass(thisDebugLevel=1)

## Create the request and capture the JSON response
#response = requests.get(thisRestUrl)
#jsonData = response.json()
#debug.debugPrint(jsonData, __DEBUG_VVV)
#
## Write the JSON to a file for future use
#dataHandling.setLocalData(localDataFolder="localData", localDataFilename="noaa15.json", jsonData=jsonData)

