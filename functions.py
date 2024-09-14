import math
import time
DAYSTOUNIX = 4371677 # 11,969 * 365.25 rounded down
DAYSINCYCLE = 1000
TOMETRIC = 1.157
SECONDSINDAY = 100000


def fetchDiff(alarm):
    seconds = loadToday()['seconds']
    diff = alarm - seconds
    if (seconds >= alarm):
        diff += SECONDSINDAY
    return diff

def incrementToday(today):
    #im implementing this so its not calculating what time it is every second
    today['seconds'] += 1
    if (today['seconds'] > SECONDSINDAY):
        today['seconds'] = 1
        today['date'] += 1
    if (today['date'] > DAYSINCYCLE):
        today['date'] = 1
        today['cycle'] += 1
    return today






def loadToday():
    seconds = math.floor((time.time() - 50000) * TOMETRIC) #the 50k is to have it start at noon instead of midnight
    days = DAYSTOUNIX + math.floor(seconds / SECONDSINDAY)
    seconds = math.floor(seconds % SECONDSINDAY)
    cycle = math.floor(days / DAYSINCYCLE)
    date = math.floor(days % DAYSINCYCLE)
    return {'seconds': seconds, 'cycle': cycle, 'date': date}
