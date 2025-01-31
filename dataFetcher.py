from support import RestAPI, Debug

# Create a RestAPI Instance
thisRestApi = RestAPI.RestApiClass(thisDebugLevel=0)

# Fetch all the JSON data and store to file
thisRestApi.fetchAllJson()
