import curses

from functions import fetchDiff, loadToday, SECONDSINDAY

ALARMFILE = 'alarms.txt'
alarms = {
    'label': [],
    'pastDue': [], 
    'setTo': [],
    }
def addToAlarmFile(value, label):
    with open(ALARMFILE, "a") as myfile:
        myfile.write("\n" + str(value) + ", " + label)

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
    alarms['label'] = []
    open(ALARMFILE, 'w').close()


def createAlarm(value, label):
    addToAlarmFile(value, label)
    alarms['setTo'].append(value)
    alarms['pastDue'].append(False)
    alarms['label'].append(label)


def deleteAlarm(value):
    id = alarms['setTo'].index(value)
    del alarms['pastDue'][id]
    del alarms['setTo'][id]
    del alarms['label'][id]
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
        alarmLabel = ""
        if (alarms['label'][id] != ''):
            alarmLabel = " (" + alarms['label'][id] + ")"
        possTxt += alarmLabel + " [" + format(fetchDiff(alarm), ',') + "]"

        if (alarms['pastDue'][id]):            
            possTxt = "-"            
            possTxt = format(alarm, ',') + alarmLabel            
            possTxt += " [!!!]"            
        alarmTxt += possTxt    
    alarmTxt += ")"
    return alarmTxt

def loadAlarms():
    with open(ALARMFILE) as file:
        while line := file.readline():
            if (line == "\n"):
                continue
            splitLine = line.split(',')
            value = int(splitLine[0].rstrip())
            label = splitLine[1].strip()
            if (value > SECONDSINDAY):
                continue
            if (value not in alarms['setTo']):
                createAlarm(value, label)
                continue
