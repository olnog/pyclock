from functions import *
from processInput import processInput
import curses
from threading import Thread
from queue import Queue, Empty
INCREMENTTODAYEVERY = 1000
LOADEVERY = 10
today = loadToday()

'''
TODO:
    be able to start the timer in the future
    have it display when solar noon is and dusk and dawn
    also display earth time  

BUGS:
 DONE: i shouldn't be able to put an alarm that is larger than 100
when you add a new alarm after an alarm has been cleared, it starts newlining like crazy
'''


loadAlarms()
loadTimers(today['seconds'])

commandQueue = Queue()

stdscr = curses.initscr()
stdscr.keypad(True)

upperwin = stdscr.subwin(2, 80, 0, 0)
lowerwin = stdscr.subwin(2,0)

def outputThreadFunc(today):
    while True:
        inputTxt = ''
        upperwin.clear()
        if (today['seconds'] % INCREMENTTODAYEVERY == 0):
            today = loadToday()
        else: 
            today = incrementToday(today)
        alarmTxt = ""
        if (today['seconds'] % LOADEVERY == 0):
            loadAlarms()
            loadTimers(today['seconds'])

        try:
            input = commandQueue.get(timeout=0.1)
            if input == 'q' or input == 'x':
                return
            inputTxt = processInput(input)
        except Empty:
            pass

        alarmTxt = displayAlarms(today['seconds'])
        upperwin.addstr(str(today['cycle']) + "-" + str(today['date']) + ": " + format(today['seconds'], ',') + " (" + alarmTxt + ")" + inputTxt)
        
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