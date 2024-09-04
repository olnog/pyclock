import math
import time

ALARMFILE = 'alarms.txt'
DAYSTOUNIX = 4371677 # 11,969 * 365.25 rounded down
DAYSINCYCLE = 1000
TOMETRIC = 1.157
SECONDSINDAY = 100000
TIMERFILE = 'timers.txt'


alarms = []
alarmsTriggered = []
timers = []
originalTimers = []
def createTimer (timer, original):    
    alarmsTriggered.append(False)
    alarms.append(None)
    originalTimers.append(original)
    timers.append(timer)

def decrementTimers():
    for id, timer in enumerate(timers):
        timers[id]-= 1
def displayAlarms(seconds):
    alarmTxt = ""
    for id, alarm in enumerate(alarms):

        if (alarmTxt != ""):
            alarmTxt += ", "                
        possTxt = "-"
        if (alarm != None):
            possTxt = format(alarm, ',') 
        possTxt += " [" + format(timers[id], ',') + "]"
        if (alarmsTriggered[id] or (timers[id] < 0)):
            possTxt = format(alarm, ',') + " [!!!]"
            alarmsTriggered[id] = True
        alarmTxt += possTxt    
    return alarmTxt

def fetchDiff(seconds, alarm):
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

def loadAlarms(seconds):
    deletedAlarms = []
    for id, element in enumerate(alarms):
        deletedAlarms.append(True)
    with open(ALARMFILE) as file:
        while line := file.readline():
            if (line == "\n"):
                continue
            value = int(float(line.rstrip()) * 1000)
            if (value > 100):
                continue
            if (value not in alarms):
                alarms.append(value)
                alarmsTriggered.append(False)
                originalTimers.append(None)
                timers.append(fetchDiff(seconds, value))
                deletedAlarms.append(False)
                continue
            deletedAlarms[alarms.index(value)] = False
    deletingValues = []
    for id, deleting in enumerate(deletedAlarms):        
        if (deleting and alarms[id] != None ):
            deletingValues.append(alarms[id])

    for elid, value in enumerate(deletingValues):
        print ("\n alarm for " + str(value) + " deleted")
        id = alarms.index(value)
        del alarmsTriggered[id]
        del alarms[id]

def loadTimers(seconds):    

    with open(TIMERFILE) as file:
        while line := file.readline():
            if (line == "\n"):
                continue
            
            if ('@' in line):
                value = line.split('@');
                timer = int(float(value[0].rstrip()) * 1000)  
                startsAt = int(float(value[1].rstrip()) * 1000)                
                diff = seconds - startsAt
                timer -= diff                
                if (line not in originalTimers and timer > 0):
                    createTimer(timer, line)
                continue


            value = int(float(line.rstrip()) * 1000)            
            if (value not in originalTimers):                
                createTimer(value, value)
                continue

def loadToday():
    seconds = math.floor((time.time() - 50000) * TOMETRIC) #the 50k is to have it start at noon instead of midnight
    days = DAYSTOUNIX + math.floor(seconds / SECONDSINDAY)
    seconds = math.floor(seconds % SECONDSINDAY)
    cycle = math.floor(days / DAYSINCYCLE)
    date = math.floor(days % DAYSINCYCLE)
    return {'seconds': seconds, 'cycle': cycle, 'date': date}
