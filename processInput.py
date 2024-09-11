from functions import createAlarm

def processInput(input):
    splitInput = input.split(' ')
    inputTxt = ''
    if splitInput[0] == 'a':
        inputTxt = "\n ALARM INPUTTED " + splitInput[1]
        createAlarm(int(float(splitInput[1]) * 1000))
        
    
    return inputTxt
        