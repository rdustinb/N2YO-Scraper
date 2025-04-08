from support import dataHandling, utils, eventFormatter
from time import strftime, localtime
import configparser, requests, json
import os,sys

################################
# Get the configuration
# Create a config parser object
config = configparser.ConfigParser()

# Read the configuration file (this just needs to be relative to the top executable)
config.read('config.ini')

# Access values from the configuration file
myLocation              = config.get('caldav', 'myLocation')
myAlertTime             = config.getint('caldav', 'myAlertTime')
outFolder               = config.get('caldav', 'outFolder')
filterAllowStart        = config.get('caldav', 'filterAllowStart')
filterAllowEnd          = config.get('caldav', 'filterAllowEnd')
printMetrics            = config.getboolean('caldav', 'printMetrics')

theseNoradIds           = config.get('satellites', 'mySatelliteNoradIds').split()
theseNames              = config.get('satellites', 'mySatelliteNames').split()

theseMetrics = list()

if filterAllowStart == "None" or filterAllowEnd == "None":
    theseMetrics.append("Filtering window is disabled...")
else:
    theseMetrics.append("Filtering window is enabled...")

################################
# Loop through all configured satellites
if os.path.isdir(outFolder):
    for thisNoradId, thisName in zip(theseNoradIds, theseNames):
        thisFilename = "%s_%s.json"%(thisNoradId, thisName)
    
        prunedEvents = 0
    
        # Read the Satellite JSON data
        thisSatelliteJson = dataHandling.getLocalData("./localData", thisFilename)
        
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
        
        # Loop through all Events for this satellite
        for thisEvent in thisSatelliteJson['passes']:
            filteredEvents = 0
            # Compare filter window start/end times with this event's start/end times
            # Event times are UTC
            # Filter Window times are local
            if filterAllowStart != "None" and filterAllowEnd != "None":
                localStartTime = strftime('%H%M', localtime(thisEvent['startUTC']))
                localFilterStartTime = filterAllowStart
                localEndTime = strftime('%H%M', localtime(thisEvent['endUTC']))
                localFilterEndTime = filterAllowEnd
                if int(localStartTime) < int(localFilterStartTime) or int(localEndTime) > int(localFilterEndTime):
                    filteredEvents += 1
                    continue

            # Generate this event's UID
            thisEventUid = "%s-%s-%s-%s"%(
                thisSatelliteJson['info']['satid'],
                thisEvent['startUTC'],
                thisEvent['maxUTC'],
                thisEvent['endUTC']
            )
    
            # Look for similarly-named events, pruning them if needed...
            searchDir = os.fsencode(outFolder)
            newStartUTC = int(thisEvent['startUTC'])
            newMaxUTC = int(thisEvent['maxUTC'])
            newEndUTC = int(thisEvent['endUTC'])
            # Loop through all files in the folder...
            for file in os.listdir(searchDir):
                filename = os.fsdecode(file)
                # Only look at the ics files...
                if filename.endswith(".ics"):
                    # For this event, the satellite ID must match
                    if filename.find("%s"%(thisSatelliteJson['info']['satid'])) != -1:
                        # Remove any files whose maxUTC is within 60 minutes of the new event...
                        currentStartUTC = int(filename.split("-")[1])
                        currentMaxUTC = int(filename.split("-")[2])
                        currentEndUTC = int(filename.split("-")[3].split(".")[0])
                        # If the analyzed event is within +/- 30 minutes of the new event, it is a duplicate and should be
                        # removed...This is probably a worst-case scenario as 10day predictive windows shouldn't drift more
                        # than a few minutes either direction...
                        if ((currentStartUTC > (newStartUTC - 1800)) and (currentStartUTC < (newStartUTC + 1800))) or \
                        ((currentMaxUTC > (newMaxUTC - 1800)) and (currentMaxUTC < (newMaxUTC + 1800))) or \
                        ((currentEndUTC > (newEndUTC - 1800)) and (currentEndUTC < (newEndUTC + 1800))):
                            # Also, only remove the file if the filename isn't EXACTLY like the new one
                            if filename != "%s.ics"%(thisEventUid):
                                print("Pruning the file %s/%s..."%(outFolder,filename))
                                os.remove("%s/%s"%(outFolder,filename))
                                prunedEvents += 1
    
            # Setup the Summary and Description strings:
            eventSummary = "%s ::: Elev %.2f"%(
                thisSatelliteJson['info']['satname'],
                thisEvent['maxEl']
            )
            eventDescription = "Start: %s; Peak: %s; End: %s"%(
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
            dataHandling.storeRawData(
                localDataFolder=outFolder,
                localDataFilename="%s.ics"%(thisEventUid),
                fileData=newEvent
            )
    
        theseMetrics.append("%s had %d events pruned due to duplication."%(thisSatelliteJson['info']['satname'], prunedEvents))
        if filterAllowStart != "None" and filterAllowEnd != "None":
            theseMetrics.append("%s had %d events filtered based on time."%(thisSatelliteJson['info']['satname'], filteredEvents))
else:
    theseMetrics.append("The out folder %s doesn't exist!"%(outFolder))

# Print the metrics to a file
if printMetrics:
    with open("metrics.log", "a+") as fh_metrics:
        for thisMetric in theseMetrics:
            fh_metrics.write("%s\n"%(thisMetric))
