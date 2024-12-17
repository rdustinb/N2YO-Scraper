from config import config
from support import dataHandling
import requests
import json

# Configure the API settings
config.setPredictionDaySpan(3)
config.setMinimumApparentElevation(35)
config.setNoradId(config.NOAA15ID)

# Generate the REST API URL
thisRestUrl = config.buildUrl()

# Debug
print("The Radio Passes URL is set as:")
print("%s"%thisRestUrl)

# Create the request and capture the JSON response
#response = requests.get(thisRestUrl)
#jsonData = response.json()

jsonData = '{ test: [1, 2, 3, 4, 5], test2: [6, 7, 8, 9, 10], test3: [0, 0, 0, 0, 0] }'

print(jsonData)

# Write the JSON to a file for future use
dataHandling.setLocalData(localDataFolder="localData", localDataFilename="test.json", jsonData=jsonData)
#dataHandling.setLocalData(localDataFolder="localData", localDataFilename="noaa15.json", jsonData=jsonData)

# Verify the stored JSON data
dataHandling.checkStoredLocalData(localDataFolder="localData", localDataFilename="test.json", jsonData=jsonData)
