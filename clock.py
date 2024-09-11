from functions import *
import curses

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


loadAlarms(today['seconds'])
loadTimers(today['seconds'])
'''
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
    curses.initscr()
    print (str(today['cycle']) + "-" + str(today['date']) + ": " + format(today['seconds'], ',') + " (" + alarmTxt + ")", end="\r")
    
    decrementTimers()
    time.sleep(.864)
'''
commandQueue = Queue()

stdscr = curses.initscr()
stdscr.keypad(True)

upperwin = stdscr.subwin(2, 80, 0, 0)
lowerwin = stdscr.subwin(2,0)

def outputThreadFunc():
    outputs = ["So this is another output","Yet another output","Is this even working"] # Just for demo
    while True:
        upperwin.clear()
        upperwin.addstr(f"{choice(outputs)}")
        try:
            inp = commandQueue.get(timeout=0.1)
            if inp == 'exit':
                return
            else:
                upperwin.addch('\n')
                upperwin.addstr(inp)
        except Empty:
            pass

        upperwin.refresh()
        sleep(.864)
        


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
            if command == 'exit':
                return

            
        


# MAIN CODE
outputThread = Thread(target=outputThreadFunc)
inputThread = Thread(target=inputThreadFunc)
outputThread.start()
inputThread.start()
outputThread.join()
inputThread.join()

stdscr.keypad(False)
curses.endwin()
print("Exit")