import curses

from functions import fetchDiff, loadToday, SECONDSINDAY

ALARMFILE = 'alarms.txt'
alarms = {
    'pastDue': [], 
    'setTo': [],
    }
def addToAlarmFile(value):
    with open(ALARMFILE, "a") as myfile:
        myfile.write("\n" + str(value))

def checkAlarms():
    seconds = loadToday()['seconds']
    for id, alarm in enumerate(alarms['setTo']):
        if (alarms['pastDue'][id]):
            continue
        if alarm - seconds < 0:
            curses.flash()
            curses.beep()
            alarms['pastDue'][id] = True


def clearAlarms():
    alarms['setTo'] = []
    alarms['pastDue'] = []
    open(ALARMFILE, 'w').close()


def createAlarm(value):
    addToAlarmFile(value)
    alarms['setTo'].append(value)
    alarms['pastDue'].append(False)
    


def deleteAlarm(value):
    id = alarms['setTo'].index(value)
    del alarms['pastDue'][id]
    del alarms['setTo'][id]
    with open(ALARMFILE, "r") as fp:
        lines = fp.readlines()
    with open(ALARMFILE, "w") as fp:
        for line in lines:
            if line.strip("\n") != value:
                fp.write(line)

def displayAlarms():
    
    if (len(alarms['setTo']) == 0):
        return ""
    alarmTxt = "(a: "
    for id, alarm in enumerate(alarms['setTo']):
        if (alarmTxt != "(a: "):
            alarmTxt += ", "                
        possTxt = "-"
        if (alarm != None):
            possTxt = format(alarm, ',') 
        possTxt += " [" + format(fetchDiff(alarm), ',') + "]"

        if (alarms['pastDue'][id]):            
            possTxt = "-"            
            possTxt = format(alarm, ',')
            possTxt += " [!!!]"            
        alarmTxt += possTxt    
    alarmTxt += ")"
    return alarmTxt

def loadAlarms():
    with open(ALARMFILE) as file:
        while line := file.readline():
            if (line == "\n"):
                continue
            value = int(line.rstrip())
            if (value > SECONDSINDAY):
                continue
            if (value not in alarms['setTo']):
                createAlarm(value)
                continue
