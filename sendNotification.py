import http.client, urllib

# Setup the Pushover account and create a unique application key
myUserKey = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
myApiKey = 'yyyyyyyyyyyyyyyyyyyyyyyyyyyyyy'

# This expects the metrics.log file to be present in the same directory.
# If running the dataFetcher and calendarWriter scripts from this directory,
# the metrics.log file will be created, if configured to do so...
#
# The entire metrics.log file will be sent as the body of the notification.
with open("metrics.log", "r") as fh_metrics:
    myMessage = ''.join(fh_metrics.readlines())

conn = http.client.HTTPSConnection("api.pushover.net:443")

conn.request("POST", "/1/messages.json",
  urllib.parse.urlencode({
    "token": myApiKey,
    "user": myUserKey,
    "message": myMessage,
  }), { "Content-type": "application/x-www-form-urlencoded" })

thisResponse = conn.getresponse()

print(thisResponse.getcode())
