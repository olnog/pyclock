from alarms import alarms, checkAlarms, displayAlarms, loadAlarms
from earth import fetchDusk, fetchEarthTime
from functions import *
from processInput import processInput
import curses
from threading import Thread
from timers import decrementTimers, displayTimers, loadTimers
from queue import Queue, Empty
INCREMENTTODAYEVERY = 1000
today = loadToday()
universalTime = True
'''
TODO:
    for earth time, don't have it be dependent on today's solar noon if that's already passed 
BUGS:
 DONE: i shouldn't be able to put an alarm that is larger than 100
when you add a new alarm after an alarm has been cleared, it starts newlining like crazy
'''



def outputThreadFunc(today, universalTime):
    while True:
        alarmTxt = ""
        inputTxt = ''        
        upperwin.clear()

        if (today['seconds'] % INCREMENTTODAYEVERY == 0):
            today = loadToday()
        else: 
            today = incrementToday(today)

        try:
            input = commandQueue.get(timeout=0.1)
            if input == 'q' or input == 'x':
                return
            inputTxt = processInput(input)
            if "EARTH" in inputTxt and universalTime == True:
                universalTime = inputTxt.split(':')[1]
            elif 'UNIVERSAL' in inputTxt and universalTime != True:
                universalTime = True

        except Empty:
            pass
        checkAlarms()
        alarmTxt = displayAlarms()
        timerTxt = displayTimers()
        clockTxt = str(today['cycle']) + "-" + str(today['date']) + ": " + format(today['seconds'], ',') + " " + alarmTxt + timerTxt + inputTxt
        earthTime = False
        if universalTime != True:
            earthTime = fetchEarthTime(universalTime)
        if earthTime == False and universalTime != True:
            universalTime = True
        if universalTime != True:
            #print (earthTime)
            clockTxt = earthTime
        upperwin.addstr(clockTxt)
        decrementTimers()        
        upperwin.refresh()
        time.sleep(.864)
        
def inputThreadFunc():
    while True:
        global buffer
        lowerwin.addstr("->")
        command = lowerwin.getstr()
        if command:
            command = command.decode("utf-8")
            commandQueue.put(command)
            lowerwin.clear()
            lowerwin.refresh()
            if command == 'q' or command == 'x':
                return

loadAlarms()
loadTimers()

commandQueue = Queue()
stdscr = curses.initscr()
stdscr.keypad(True)
upperwin = stdscr.subwin(10, 80, 0, 0)
lowerwin = stdscr.subwin(2,0)            
        
# MAIN CODE

outputThread = Thread(target=outputThreadFunc, args=(today, universalTime))
inputThread = Thread(target=inputThreadFunc)
outputThread.start()
inputThread.start()
outputThread.join()
inputThread.join()

stdscr.keypad(False)
curses.endwin()
print("Exit")
