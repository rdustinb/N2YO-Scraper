
################################################################################
#                               Description
################################################################################
# The purpose of this script is to read in a local .json file which contains 
# information about a satellite's sky traversions and convert each event into
# a single CalDav file with a unique UUID as a filename.

#############################################
# Structure of a CalDav File
#############################################

# The RFC of the specification can be found here:
# https://www.rfc-editor.org/rfc/rfc4791
#
################################
# Boilerplate
################################
# BEGIN:VCALENDAR
#   VERSION:2.0
#   CALSCALE:GREGORIAN
#   PRODID:-//Apple Inc.//macOS 13.7.1//EN
################################
# Timezone Information
################################
#   BEGIN:VTIMEZONE
#       TZID:America/Denver
################################
# Daylight Savings Starts
################################
#       BEGIN:STANDARD
#           DTSTART:20071104T020000
#           RRULE:FREQ=YEARLY;BYMONTH=11;BYDAY=1SU
#           TZNAME:MST
#           TZOFFSETFROM:-0600
#           TZOFFSETTO:-0700
#       END:STANDARD
################################
# Daylight Savings Ends
################################
#       BEGIN:DAYLIGHT
#           DTSTART:20070311T020000
#           RRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=2SU
#           TZNAME:MDT
#           TZOFFSETFROM:-0700
#           TZOFFSETTO:-0600
#       END:DAYLIGHT
#   END:VTIMEZONE
################################
# Visible Event Information
################################
#   BEGIN:VEVENT
#       SUMMARY:Yet Another Test Event
#       DTSTART;TZID=America/Denver:20250131T120000
#       DTEND;TZID=America/Denver:20250131T121500
#       LOCATION:Location: Space
#       DESCRIPTION:Some notes about the event.
#       URL;VALUE=URI:www.website.com
################################
# Invisible Event Information
################################
#       UID:00000000-1111-2222-3333-444444444444
#       # RFC4791, section 7.10 - this is the default, allows for determining free/busy
#       TRANSP:OPAQUE
#       SEQUENCE:0
#       CREATED:20250129T034026Z
#       LAST-MODIFIED:20250129T042506Z
#       DTSTAMP:20250129T042506Z
################################
# Alarm/Reminder Information
################################
#       BEGIN:VALARM
#           ACTION:DISPLAY
#           DESCRIPTION:Reminder
#           TRIGGER:-PT15M
#           UID:E1CD3F83-3AB9-46CC-8048-508A4E65D01B
#           X-WR-ALARMUID:E1CD3F83-3AB9-46CC-8048-508A4E65D01B
#       END:VALARM
#   END:VEVENT
# END:VCALENDAR

################################################################################
#                                   Support
################################################################################
from support import utils

################################################################################
#                                  Time Stuff
################################################################################
import datetime, dateutil

def utcEpochToLocalTime(thisEpoch: int, myLocationString: str):
    # Convert the Epoch Time to a Timestamp object of the UTC timezone
    thisUtcTime = datetime.datetime.fromtimestamp(thisEpoch).replace(tzinfo=dateutil.tz.gettz(myLocationString))
    #thisUtcTime = datetime.datetime.fromtimestamp(thisEpoch).replace(tzinfo=dateutil.tz.gettz('UTC'))
    # Convert the UTC Timestamp object to a Local Timestamp object
    thisLocalTime = thisUtcTime.astimezone(dateutil.tz.gettz(myLocationString))
    # Format the timestamp to YYYYMMDDTHHMMSS
    thisLocalTimeFormatted = thisLocalTime.strftime("%Y%m%dT%H%M%S")
    # Return the local time
    return thisLocalTimeFormatted

def getCurrentLocalTime():
    return datetime.datetime.now().strftime("%Y%m%dT%H%M%S")

def getTimezoneInfo(thisTime: str, myLocationString: str):
    # Generate the TZ Object for the location
    thisTz = dateutil.tz.gettz(myLocationString)

    # Get the TZ Offset and Name for this specific time
    thisTzOffset = datetime.datetime.strptime(thisTime, "%Y%m%dT%H%M%S").replace(tzinfo=thisTz).strftime("%z")
    thisTzName = datetime.datetime.strptime(thisTime, "%Y%m%dT%H%M%S").replace(tzinfo=thisTz).strftime("%Z")

    # Return the values
    return thisTzOffset, thisTzName

################################################################################
#                             Calendar Event Building
################################################################################
def generateVALARM(minutesBefore: int):
    newAlarmList = list()

    # Of the form xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    thisAlarmUID = utils.genRandomId()

    # Append the alarm information
    newAlarmList.append("BEGIN:VALARM")
    newAlarmList.append("ACTION:DISPLAY")
    newAlarmList.append("DESCRIPTION:Reminder")
    newAlarmList.append("TRIGGER:-PT%iM"%(minutesBefore))
    newAlarmList.append("UID:%s"%(thisAlarmUID))
    newAlarmList.append("X-WR-ALARMUID:%s"%(thisAlarmUID))
    newAlarmList.append("END:VALARM")

    # Return the new list
    return newAlarmList

def generateVEVENT(eventSummary: str, startTime: str, endTime: str, myLocationString: str, 
                  eventLocation: str, eventDescription: str, eventUrl: str, eventUid: str,
                   alarmMinutesBefore: int):
    newEventList = list()

    # Convert the Start time to local in the correct format
    localStartTime = utcEpochToLocalTime(thisEpoch=startTime, myLocationString=myLocationString)
    # Convert the End time to local in the correct format
    localEndTime = utcEpochToLocalTime(thisEpoch=endTime, myLocationString=myLocationString)
    # Create the current timestamp
    thisCurrentTime = getCurrentLocalTime()

    # Create a list of the event information
    newEventList.append("BEGIN:VEVENT")
    newEventList.append("SUMMARY:%s"%(eventSummary))
    newEventList.append("DTSTART;TZID=%s:%s"%(myLocationString,localStartTime))
    newEventList.append("DTEND;TZID=%s:%s"%(myLocationString,localEndTime))
    newEventList.append("LOCATION:%s"%(eventLocation))
    newEventList.append("DESCRIPTION:%s"%(eventDescription))
    newEventList.append("URL;VALUE=URI:%s"%(eventUrl))
    newEventList.append("UID:%s"%(eventUid))
    newEventList.append("TRANSP:OPAQUE")
    newEventList.append("SEQUENCE:0")
    newEventList.append("CREATED:%s"%(thisCurrentTime))
    newEventList.append("LAST-MODIFIED:%s"%(thisCurrentTime))
    newEventList.append("DTSTAMP:%s"%(thisCurrentTime))

    # Generate and append an alert/reminder to the event
    alarmList = generateVALARM(minutesBefore=alarmMinutesBefore)

    # Add the alarm list to the new event list
    newEventList.extend(alarmList)

    # Close the event
    newEventList.append("END:VEVENT")

    # Return the new list
    return newEventList

def generateVTIMEZONE(myLocationString: str):
    newTimezoneList = list()

    # Get the Offset and Name
    startOffset, startName = getTimezoneInfo(thisTime="20071104T020000", myLocationString=myLocationString)
    endOffset, endName = getTimezoneInfo(thisTime="20070311T020000", myLocationString=myLocationString)

    # This is static until Daylight savings changes in the US
    newTimezoneList.append("BEGIN:VTIMEZONE")
    newTimezoneList.append("TZID:%s"%(myLocationString))
    newTimezoneList.append("BEGIN:STANDARD")
    newTimezoneList.append("DTSTART:20071104T020000")
    newTimezoneList.append("RRULE:FREQ=YEARLY;BYMONTH=11;BYDAY=1SU")
    newTimezoneList.append("TZNAME:%s"%(startName))
    newTimezoneList.append("TZOFFSETFROM:%s"%(endOffset))
    newTimezoneList.append("TZOFFSETTO:%s"%(startOffset))
    newTimezoneList.append("END:STANDARD")
    newTimezoneList.append("BEGIN:DAYLIGHT")
    newTimezoneList.append("DTSTART:20070311T020000")
    newTimezoneList.append("RRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=2SU")
    newTimezoneList.append("TZNAME:%s"%(endName))
    newTimezoneList.append("TZOFFSETFROM:%s"%(startOffset))
    newTimezoneList.append("TZOFFSETTO:%s"%(endOffset))
    newTimezoneList.append("END:DAYLIGHT")
    newTimezoneList.append("END:VTIMEZONE")

    # Return the new list
    return newTimezoneList

def generateCalDavEvent(eventSummary: str, startTime: str, endTime: str, myLocationString: str, 
                  eventLocation: str, eventDescription: str, eventUrl: str, eventUid: str,
                   alarmMinutesBefore: int):

    # Due to the Time Location String needing quotes in some places but not others, clean the value to be sure
    myLocationString = myLocationString.strip("'").strip("\"")

    newCalendarEntryList = list()

    newCalendarEntryList.append("BEGIN:VCALENDAR")
    newCalendarEntryList.append("VERSION:2.0")
    newCalendarEntryList.append("CALSCALE:GREGORIAN")
    newCalendarEntryList.append("PRODID:-//N2YO Scraper//Version 1.0//EN")

    # Generate the timezone fields
    timezoneList = generateVTIMEZONE(myLocationString=myLocationString)

    # Generate base event fields
    eventList = generateVEVENT(
        eventSummary=eventSummary,
        startTime=startTime,
        endTime=endTime,
        myLocationString=myLocationString,
        eventLocation=eventLocation,
        eventDescription=eventDescription,
        eventUrl=eventUrl,
        eventUid=eventUid,
        alarmMinutesBefore=alarmMinutesBefore
    )

    # Add the timezone list to the new calendar entry
    newCalendarEntryList.extend(timezoneList)

    # Add the base event list to the new calendar entry
    newCalendarEntryList.extend(eventList)
    
    # Close the calendar entry
    newCalendarEntryList.append("END:VCALENDAR")

    # Return the full event
    return newCalendarEntryList
