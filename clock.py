import math
import time
DAYSTOUNIX = 4371677 # 11,969 * 365.25 rounded down
DAYSINCYCLE = 1000
TOMETRIC = 1.157
SECONDSINDAY = 100000
while 1==1:  
    seconds = math.floor((time.time() - 50000) * TOMETRIC)
    days = DAYSTOUNIX + math.floor(seconds / SECONDSINDAY)
    seconds = math.floor(seconds % SECONDSINDAY)
    cycle = math.floor(days / DAYSINCYCLE)
    date = math.floor(days % DAYSINCYCLE)

    print (str(cycle) + "-" + str(date) + ": " + format(seconds, ','), end="\r")
    time.sleep(.864)