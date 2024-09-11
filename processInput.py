from functions import *

def processInput(input):
    splitInput = input.split(' ')
    inputTxt = ''
    if splitInput[0] == 'a':
        inputTxt = "\n ADDING ALARM " + splitInput[1]
        addToAlarmFile(splitInput[1])
        createAlarm(int(float(splitInput[1]) * 1000))
        loadAlarms()
    elif splitInput[0] == 'd':
        inputTxt = "\n DELETING ALARM " + splitInput[1]
        deleteAlarm(splitInput[1])
        loadAlarms()
    
    return inputTxt
        