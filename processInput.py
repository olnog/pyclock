#from functions import *
from alarms import clearAlarms, createAlarm, deleteAlarm
from timers import clearTimers, parseTimerInput
def processInput(input):
    splitInput = input.split(' ')
    inputTxt = ''
    if splitInput[0] == 'a':
        inputTxt = "\n ADDING ALARM " + splitInput[1]
        createAlarm(int(float(splitInput[1]) * 1000))
    elif splitInput[0] == 'ac':
        inputTxt = "\n CLEARING ALARMS"
        clearAlarms()
    elif splitInput[0] == 'd':
        inputTxt = "\n DELETING ALARM " + splitInput[1]
        deleteAlarm(splitInput[1])
    elif splitInput[0] == 't':
        inputTxt = "\n " + parseTimerInput(splitInput[1])    
    elif splitInput[0] == 'tc':
        inputTxt = "\n CLEARING TIMERS"
        clearTimers()
    return inputTxt
        