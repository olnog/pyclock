from alarms import checkAlarms, displayAlarms, loadAlarms
from functions import *
from processInput import processInput
import curses
from threading import Thread
from timers import decrementTimers, displayTimers, loadTimers
from queue import Queue, Empty
INCREMENTTODAYEVERY = 1000
LOADEVERY = 10 #got rid of this because I can do it on the fly now
today = loadToday()

'''
TODO:
    have it display when solar noon is and dusk and dawn
    also display earth time  q

BUGS:
 DONE: i shouldn't be able to put an alarm that is larger than 100
when you add a new alarm after an alarm has been cleared, it starts newlining like crazy
'''

loadAlarms()
loadTimers()
commandQueue = Queue()
stdscr = curses.initscr()
stdscr.keypad(True)
upperwin = stdscr.subwin(2, 80, 0, 0)
lowerwin = stdscr.subwin(2,0)

def outputThreadFunc(today):
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
        except Empty:
            pass
        checkAlarms()
        alarmTxt = displayAlarms()
        timerTxt = displayTimers()
        upperwin.addstr(str(today['cycle']) + "-" + str(today['date']) + ": " + format(today['seconds'], ',') + " " + alarmTxt + timerTxt + inputTxt)
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

            
        


# MAIN CODE
outputThread = Thread(target=outputThreadFunc, args=(today,))
inputThread = Thread(target=inputThreadFunc)
outputThread.start()
inputThread.start()
outputThread.join()
inputThread.join()

stdscr.keypad(False)
curses.endwin()
print("Exit")