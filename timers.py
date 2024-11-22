from functions import loadToday
from alarms import createAlarm
TIMERFILE = 'timers.txt'

timers = {
    'setTo': [],
    'remaining': [],
    'started': [],
}

def checkTimers():
    for id, timer in enumerate(alarms['remaining']):
        if timer < 0:
            curses.flash()
            curses.beep()            

def clearTimers():
    timers['setTo'] = []
    timers['remaining'] = []
    timers['started'] = []

def createTimer (setTo, remaining, started):        
    timers['setTo'].append(setTo)
    timers['remaining'].append(remaining) # is there a scenario where the remaining time would NOT be the time set?
    timers['started'].append(started)

def displayTimers():
    
    if (len(timers['remaining']) == 0):
        return ""
    timerTxt = "(t: "
    for id, timer in enumerate(timers['remaining']):
        if (timerTxt != "(t: "):
            timerTxt += ", "                
        
        possTxt = " " + format(timer, ',') 
        if (timer < 1 and timers['started'][id] == None):                        
            possTxt = " !!!"
        elif (timer < 1 and timers['started'][id] != None):
            possTxt = " !!" + str(timers['started'][id]) + "k!!"
        possTxt += "/" 
        
        timerSetTo = format(timers['setTo'][id], ',')
        timerTxt += possTxt + timerSetTo
    timerTxt += ")"
    return timerTxt

def decrementTimers():
    for id, timer in enumerate(timers['remaining']):        
        timers['remaining'][id] -= 1

def loadTimers():    
    seconds = loadToday()['seconds']
    with open(TIMERFILE) as file:
        while line := file.readline():
            if (line == "\n"):
                continue
            
            parseTimerInput(line)


def parseTimerInput(input):
    seconds = loadToday()['seconds']
    if ('@' in input):
        value = input.split('@')
        timer = int(float(value[0].rstrip()) * 1000)  
        startsAt = int(float(value[1].rstrip()) * 1000)                
        diff = seconds - startsAt
        remaining = timer - diff                
        setAlarmTo = startsAt + timer
        createAlarm ( setAlarmTo)
        #if (input not in timers['setTo'] and timer > 0):
            #createTimer(timer, remaining, value[1])
        return "CREATING TIMER FOR " + str(timer) + "s (" + str(input) + ")"
    
    value = int(float(input.rstrip()) * 1000) 

    setAlarmTo = (seconds + value)   
    createAlarm(setAlarmTo)           
    return "CREATING TIMER FOR " + str(value)
    #if (value not in timers['setTo']):                
        #createTimer(value, value, None)
     