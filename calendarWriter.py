
#############################################
# Structure of a CalDav File
#############################################
# The RFC of the specification can be found here:
# https://www.rfc-editor.org/rfc/rfc4791
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
#
#       BEGIN:VALARM
#           ACTION:NONE
#           TRIGGER;VALUE=DATE-TIME:19760401T005545Z
#       END:VALARM
#   END:VEVENT
# END:VCALENDAR

import uuid

def genRandomId():
    # See RFC4122 for more information as this package generates random UUIDs based on that specification:
    # https://www.rfc-editor.org/rfc/rfc4122
    #
    # The function uuid1, uuid3, uuid4, and uuid5 provide the different versions of UUIDs
    return str(uuid.uuid4())

def generateAlert(minutesBefore: int):
    newDataList = list()

    # Of the form xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    thisAlarmUID = genRandomId()

    # Append the alarm information
    newDataList.append("BEGIN:VALARM")
    newDataList.append("ACTION:DISPLAY")
    newDataList.append("DESCRIPTION:Reminder")
    newDataList.append("TRIGGER:-PT%iM"%(minutesBefore))
    newDataList.append("UID:%s"%(thisAlarmUID))
    newDataList.append("X-WR-ALARMUID:%s"%(thisAlarmUID))
    newDataList.append("END:VALARM")
    newDataList.append("BEGIN:VALARM")
    newDataList.append("ACTION:NONE")
    newDataList.append("TRIGGER;VALUE=DATE-TIME:19760401T005545Z")
    newDataList.append("END:VALARM")

    # Return the new list
    return newDataList

import datetime, dateutil

def utcEpochToLocalTime(thisEpoch: int, myTimezone: str):
    # Convert the Epoch Time to a Timestamp object of the UTC timezone
    thisUtcTime = datetime.datetime.fromtimestamp(thisEpoch).replace(tzinfo=dateutil.tz.gettz('UTC'))
    # Convert the UTC Timestamp object to a Local Timestamp object
    thisLocalTime = thisUtcTime.astimezone(dateutil.tz.gettz(myTimezone))
    # Format the timestamp to YYYYMMDDTHHMMSS
    thisLocalTimeFormatted = thisLocal.strftime("%Y%m%dT%H%M%S")
    # Return the local time
    return thisLocalTime

def getCurrentLocalTime():
    return datetime.datetime.now().strftime("%Y%m%dT%H%M%S")

def generateEvent(eventSummary: str, startTime: str, endTime: str, myTimezone: str, 
                  eventLocation: str, eventDescription: str, eventUrl: str, eventUid: str):
    newDataList = list()

    # Convert the Start time to local in the correct format
    localStartTime = utcEpochToLocalTime(thisEpoch=startTime, myTimezone=myTimezone)
    # Convert the End time to local in the correct format
    localEndTime = utcEpochToLocalTime(thisEpoch=endTime, myTimezone=myTimezone)
    # Create the current timestamp
    thisCurrentTime = getCurrentLocalTime()

    newDataList.append("BEGIN:VEVENT")
    newDataList.append("SUMMARY:%s"%(eventSummary))
    newDataList.append("DTSTART;TZID=%s:%s"%(myTimezone,localStartTime))
    newDataList.append("DTEND;TZID=%s:%s"%(myTimezone,localEndTime))
    newDataList.append("LOCATION:Location: %s"%(eventLocation))
    newDataList.append("DESCRIPTION:%s"%(eventDescription))
    newDataList.append("URL;VALUE=URI:%s"%(eventUrl))
    newDataList.append("UID:%s"%(eventUid))
    newDataList.append("TRANSP:OPAQUE")
    newDataList.append("SEQUENCE:0")
    newDataList.append("CREATED:%s"%(thisCurrentTime))
    newDataList.append("LAST-MODIFIED:%s"%(thisCurrentTime))
    newDataList.append("DTSTAMP:%s"%(thisCurrentTime))

    # Return the new list
    return newDataList
