from functions import *
INCREMENTTODAYEVERY = 1000
LOADEVERY = 10
today = loadToday()

'''
TODO:

BUGS:
 DONE: i shouldn't be able to put an alarm that is larger than 100
when you add a new alarm after an alarm has been cleared, it starts newlining like crazy
'''


loadAlarms(today['seconds'])
loadTimers(today['seconds'])

while 1==1:

    if (today['seconds'] % INCREMENTTODAYEVERY == 0):
        today = loadToday()
    else: 
        today = incrementToday(today)
    alarmTxt = ""
    
    if (today['seconds'] % LOADEVERY == 0):
        loadAlarms(today['seconds'])
        loadTimers(today['seconds'])
    alarmTxt = displayAlarms(today['seconds'])
            
    
    
    print (str(today['cycle']) + "-" + str(today['date']) + ": " + format(today['seconds'], ',') + " (" + alarmTxt + ")", end="\r")
    
    decrementTimers()

    time.sleep(.864)