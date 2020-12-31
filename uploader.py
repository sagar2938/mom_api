import datetime

# formatted string version
minutes15 = (datetime.now() + datetime.timedelta(hours=05,minutes=15)).strftime("%H:%M")
print "in 15 minutes the time will be %s" % minutes15  # eg. 11:05:37
