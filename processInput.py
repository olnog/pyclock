from functions import convertImperial, convertMetric
from alarms import clearAlarms, createAlarm, deleteAlarm
from timers import clearTimers, parseTimerInput
def processInput(input):
    splitInput = input.split(' ')
    inputTxt = ''
    if splitInput[0] == 'a' and len(splitInput) > 1:
        inputTxt = "\n ADDING ALARM " + splitInput[1]
        createAlarm(int(float(splitInput[1]) * 1000))
    elif splitInput[0] == 'ac':
        inputTxt = "\n CLEARING ALARMS"
        clearAlarms()
    elif splitInput[0] == 'c' and len(splitInput) > 1:
        inputTxt = "\n " + splitInput[1] + " minutes equals " + format(convertImperial(int(splitInput[1])), ',') + " metric seconds"
    elif splitInput[0] == 'cm' and len(splitInput) > 1:
        inputTxt = "\n " + splitInput[1] + " metric seconds equals " + format(convertMetric(float(splitInput[1])), ',') + " minutes"

    elif splitInput[0] == 'd' and len(splitInput) > 1:
        inputTxt = "\n DELETING ALARM " + splitInput[1]    
        deleteAlarm(splitInput[1])
    elif splitInput[0] == 'e' and len(splitInput) > 1:
        inputTxt = "\n CHANGING MODE TO EARTH TIME:" + splitInput[1]        
    elif splitInput[0] == 't' and len(splitInput) > 1:
        inputTxt = "\n " + parseTimerInput(splitInput[1])    
    elif splitInput[0] == 'tc':
        inputTxt = "\n CLEARING TIMERS"
        clearTimers()
    elif splitInput[0] == 'u':
        inputTxt = "\n CHANGING MODE TO UNIVERSAL"
    elif splitInput[0] == 'z':
        inputTxt = "\n ZIPCODE IS NOW " + splitInput[1]
    return inputTxt
        