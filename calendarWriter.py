from support import dataHandling, utils, eventFormatter
import configparser, requests, json

################################
# Get the configuration
# Create a config parser object
config = configparser.ConfigParser()

# Read the configuration file (this just needs to be relative to the top executable)
config.read('config.ini')

# Access values from the configuration file
myLocation  = config.get('caldav', 'myLocation')
myAlertTime = config.getint('caldav', 'myAlertTime')
outFolder   = config.get('caldav', 'outFolder')

################################
# Write the calendar events to an ics file
thisFilename = "25338_NOAA15.json"

# Read the Satellite JSON data
thisSatelliteJson = dataHandling.getLocalData("./localData", thisFilename)

#print(thisSatelliteJson['info'])
# Passes is a list of dicts
# Each pass dict has the following keys:
# 'startAz'
# 'startAzCompass'
# 'startUTC'
# 'maxAz'
# 'maxAzCompass'
# 'maxEl'
# 'maxUTC'
# 'endAz'
# 'endAzCompass'
# 'endUTC'
#print(thisSatelliteJson['passes'][0].keys())
#for thisEvent in thisSatelliteJson['passes']:
#    print(thisEvent)

# Loop through all Events for this satellite
for thisEvent in thisSatelliteJson['passes']:
    # Generate this event's UID
    thisEventUid = utils.genRandomId()
    # Setup the Summary and Description strings:
    eventSummary = "%s, Elevation: %.2f"%(
        thisSatelliteJson['info']['satname'],
        thisEvent['maxEl']
    )
    eventDescription = "Start: %s, Peak: %s, End: %s"%(
        thisEvent['startAzCompass'],
        thisEvent['maxAzCompass'],
        thisEvent['endAzCompass']
    )
    thisUrl = "www.n2yo.com"
    # Generate the Calendar Event
    newEvent = eventFormatter.generateCalDavEvent(
      eventSummary=eventSummary,
      startTime=thisEvent['startUTC'],
      endTime=thisEvent['endUTC'],
      myLocationString=myLocation,
      eventLocation='Outer Space',
      eventDescription=eventDescription,
      eventUrl=thisUrl,
      eventUid=thisEventUid,
      alarmMinutesBefore=myAlertTime
    )
    # Write the Calendar Event to a file
    with open("%s/%s.ics"%(outFolder,thisEventUid), "w+") as fh_write:
        for thisLine in newEvent:
            fh_write.write("%s\n"%(thisLine))
