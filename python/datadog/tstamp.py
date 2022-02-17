from datetime import datetime, timedelta, timezone
from dateutil.tz import gettz
import time
import pytz

#time in Epoch or POSIX timestamp

start = 1645617000
end = 1645648200

#start=1644925368
#start_datetime = datetime(2022,2,15,19,50,0)
#end_datetime = datetime(2022,2,16,4,15,0)

#start = int(start_datetime.timestamp())
#end = int(end_datetime.timestamp())

print(f"start time: {start}")
print(f"end time: {end}")

indatetime = datetime.fromtimestamp(start)
print(f'In local time...{indatetime}')
local = pytz.timezone("Asia/Kolkata")
toconvert = pytz.timezone("Asia/Kuala_Lumpur")
localize = local.localize(indatetime)
converted = localize.astimezone(toconvert)
print(f'In converted timezone: {converted}')

#utc_time = datetime(1970, 1, 1, tzinfo=timezone.utc) + timedelta(seconds=timestamp)
#utc_time = datetime(1970, 1, 1, tzinfo=gettz('Asia/Kuala_Lumpur')) + timedelta(seconds=timestamp)
#print(utc_time)
#abcd = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start))
#abcde = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end))
#print(abcd)
#print(abcde)
# -> 2012-10-23 23:55:17.179363+00:00
