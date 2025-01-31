# Support definitions
import json
from pathlib import Path

################################
# Order the JSON Object
def ordered(jsonData):
    if isinstance(jsonData, dict):
        return sorted((k, ordered(v)) for k, v in jsonData.items())
    if isinstance(jsonData, list):
        return sorted(ordered(x) for x in obj)
    else:
        return jsonData

################################
# Store the data to a local file
def setLocalData(localDataFolder: str, localDataFilename: str, jsonData):
    localDataFilePath = Path(localDataFolder+"/"+localDataFilename)

    print("Setting data to %s"%(localDataFilePath))

    # Create the folder if it doesn't exist
    Path(localDataFolder).mkdir(parents=True, exist_ok=True)

    # Store the data local
    with open(localDataFilePath, "w") as fh:
        json.dump(jsonData, fh)

################################
# Get the data from a local file
def getLocalData(localDataFolder: str, localDataFilename: str):
    localDataFilePath = Path(localDataFolder+"/"+localDataFilename)

    print("Getting data from %s"%(localDataFilePath))

    # Read the data from the local file...
    with open(localDataFilePath, "r") as fh:
        jsonData = json.load(fh)
    return jsonData

################################
# Check Stored Data vs. Object
def checkStoredLocalData(localDataFolder: str, localDataFilename: str, jsonData):
    # Fetch the JSON data from the file...
    storedJsonData = getLocalData(localDataFolder=localDataFolder, localDataFilename=localDataFilename)

    # Compare the JSON data in the file with the JSON data from the object
    if ordered(jsonData) == ordered(storedJsonData):
        print("Data was stored correctly!")
    else:
        print("Data was NOT stored correctly!")
