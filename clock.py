import math
import time
ALARMFILE = 'alarms.txt'
DAYSTOUNIX = 4371677 # 11,969 * 365.25 rounded down
DAYSINCYCLE = 1000
TOMETRIC = 1.157
SECONDSINDAY = 100000


alarms = []
alarmsTriggered = []

def displayAlarms(seconds):
    alarmTxt = ""
    for id, alarm in enumerate(alarms):
        if (alarmsTriggered[id]):
            continue
        
        if (alarmTxt != ""):
            alarmTxt += ", "                
        diff = alarm - seconds
        if (seconds >= alarm):
            diff += SECONDSINDAY
        possTxt = format(alarm, ',') + " [" + format(diff, ',') + "]"
        if (seconds >= alarm and alarm > seconds - 10):
            possTxt = format(alarm, ',') + " [!!!]"
            alarmsTriggered[id] = True
        alarmTxt += possTxt    
    return alarmTxt

def loadAlarms():
    deletedAlarms = []
    for id, element in enumerate(alarms):
        deletedAlarms.append(True)
    with open(ALARMFILE) as file:
        while line := file.readline():
            value = int(line.rstrip()) * 1000
            if (value not in alarms):
                alarms.append(value)
                alarmsTriggered.append(False)
                deletedAlarms.append(False)
                continue
            deletedAlarms[alarms.index(value)] = False
    deletingValues = []
    for id, deleting in enumerate(deletedAlarms):        
        if (deleting):
            deletingValues.append(alarms[id])

    for elid, value in enumerate(deletingValues):
        print ("\n" + str(value) + " deleted")
        id = alarms.index(value)
        del alarmsTriggered[id]
        del alarms[id]
    

loadAlarms()
while 1==1:
    alarmTxt = ""
    seconds = math.floor((time.time() - 50000) * TOMETRIC) #the 50k is to have it start at noon instead of midnight
    days = DAYSTOUNIX + math.floor(seconds / SECONDSINDAY)
    seconds = math.floor(seconds % SECONDSINDAY)
    cycle = math.floor(days / DAYSINCYCLE)
    date = math.floor(days % DAYSINCYCLE)
    if (seconds % 25 == 0):
        loadAlarms()
    alarmTxt = displayAlarms(seconds)
            
    
    
    print (str(cycle) + "-" + str(date) + ": " + format(seconds, ',') + " (" + alarmTxt + ")", end="\r")
    
    
    time.sleep(.864)