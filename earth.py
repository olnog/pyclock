
import datetime
import time
from math import cos, degrees, floor, radians, sin, tan, asin, acos
from functions import loadToday

COORDFILE = 'zip2latlong.txt'
SECONDSINDAY = 86400
MINUTESINHOURS = 60
TIMEPASTLOCALMIDNIGHT = 0.1/24
TIMEZONE = -7
DAYSTOUNIX = 4371677
DAYSINCYCLE = 1000
METRICSECONDSINDAY = 100000
TOMETRIC = 1.157

def fetchEarthTime(zipcode):
    days = {        
        "today": { "dawn": fetchDawn(zipcode, False, False), 
             "noon": fetchSolarNoon(zipcode, False, False), 
             'dusk' : fetchDusk(zipcode, False, False) },
        "tomorrow": { "dawn": fetchDawn(zipcode, True, False), 
                "noon": fetchSolarNoon(zipcode, True, False), 
                'dusk' : fetchDusk(zipcode, True, False) } 
    }
    
    prevDays = {
        'tomorrow': 'today',
        'today': 'yesterday',
    }
    times = {}
    earthTimeString = ""
    sortArr = []
    daysArr = ['today', 'tomorrow']
    for i, day in enumerate(daysArr):        
        for id, (when, time) in enumerate(days[day].items()):                 
            diff = fetchDiff(time, True)            
            diff = floor(diff * TOMETRIC)
            if (diff > 0 and diff < METRICSECONDSINDAY):
                sortArr.append(day + "-" + when + "-" + time)                                 
    earthTime = abs(floor(fetchDiff(days['today']['noon'], True) * TOMETRIC))
    earthTimeString = "earth-time: " + format(earthTime, ",") + "\n"
    for id, val in enumerate(sortArr):
        whichDay = val.split('-')[0]
        
        when = val.split('-')[1]
        time = val.split('-')[2]
        prevDay = prevDays[whichDay]
        if (when == 'dusk'):
            prevDay = 'today'
        diff = floor (fetchDiff( days[whichDay][when], days[prevDay]['noon']) * TOMETRIC)
        diffFromNow = floor(fetchDiff(days[whichDay][when], True) * TOMETRIC)
        earthTimeString += whichDay + "'s " + when + ": "  
        if (when == 'noon'):
            earthTimeString += "0"
        else:
            earthTimeString += format(diff, ',') 

        earthTimeString += " [" + format(diffFromNow, ',') + "]\n"
        #earthTimeString += fetchDiff()
        
    #for id, (key, when) in enumerate(times.items()):
    #    earthTimeString += key + ": " + format(when, ",") + " "
        
    return earthTimeString

def fetchCoords(zipcode):
    with open(COORDFILE) as file:
        for line in file:
            lineArr = line.split(',')
            if lineArr[0].strip() == str(zipcode):
                return {'latitude': float(lineArr[1].strip()), 'longitude': float(lineArr[2].strip())}
    return None

def fetchDawn(zipcode, tomorrow, asNumber):
    dateObj = datetime.datetime.today()
    if (tomorrow):
        dateObj = datetime.datetime.today() + datetime.timedelta(days=1) 
    noon = fetchSolarNoon(zipcode, tomorrow, True)
    julianCentury = fetchJulianCentury(dateObj)

    HASunriseDegrees = fetchHASunriseDegrees(zipcode, julianCentury)
    dawnCent = noon - HASunriseDegrees * 4 / 1440
    if (asNumber):
        return dawnCent
    seconds = floor(SECONDSINDAY * dawnCent)
    timeStr = formatTime(seconds)
    return dateObj.strftime("%Y/%m/%d") + " " + timeStr

def fetchDiff(start, now):
    end = time.time()
    if (now != True):
        end = time.mktime(time.strptime(now, "%Y/%m/%d %H:%M:%S"))    
    
    
    start = time.mktime(time.strptime(start, "%Y/%m/%d %H:%M:%S"))    
    diff = start - end
    return diff

def fetchDusk(zipcode, tomorrow, asNumber):
    dateObj = datetime.datetime.today()
    if (tomorrow):
        dateObj = datetime.datetime.today() + datetime.timedelta(days=1) 
    solarNoon = fetchSolarNoon(zipcode, tomorrow, True)
    julianCentury = fetchJulianCentury(dateObj)
    HASunriseDegrees = fetchHASunriseDegrees(zipcode, julianCentury)
    duskCent = solarNoon + HASunriseDegrees * 4 / 1440
    if (asNumber):
        return duskCent
    seconds = floor(SECONDSINDAY * duskCent)
    timeStr = formatTime(seconds)
    return dateObj.strftime("%Y/%m/%d") + " " + timeStr

    


def fetchHASunriseDegrees(zipcode, julianCentury):
    coords = fetchCoords(zipcode)
    if coords == None:
        return False
    latitude = coords['latitude']
    longitude = coords['longitude']
    geomMeanLongSunDegrees = fetchGeomMeanLongSunDegrees(julianCentury)
    geomMeanAnomSunDegrees = fetchGeomMeanAnomSunDegrees(julianCentury)
    obliqCorrDegrees = fetchObliqCorrDegrees(julianCentury)
    sunEqOfCtr = sin(radians(geomMeanAnomSunDegrees)) * (1.914602 - julianCentury * (0.004817 + 0.000014 * julianCentury)) + sin(radians(2 * geomMeanAnomSunDegrees)) * (0.019993 - 0.000101 * julianCentury) + sin(radians(3 * geomMeanAnomSunDegrees)) * 0.000289
    sunTrueLongDegrees = geomMeanLongSunDegrees + sunEqOfCtr
    sunAppLongDegrees = sunTrueLongDegrees - 0.00569 - 0.00478 * sin(radians(125.04 - 1934.136 * julianCentury)) 

    sunDeclineDegrees = degrees(asin(sin(radians(obliqCorrDegrees)) * sin(radians(sunAppLongDegrees))))
    
    HASunriseDegrees = degrees(acos(cos(radians(90.833)) 
        / (cos(radians(latitude)) * cos(radians(sunDeclineDegrees))) 
        - tan(radians(latitude)) * tan(radians(sunDeclineDegrees))))
    return HASunriseDegrees

def fetchGeomMeanAnomSunDegrees(julianCentury):
    geomMeanAnomSunDegrees = 357.52911 + julianCentury * (35999.05029 - 0.0001537 * julianCentury)
    return geomMeanAnomSunDegrees

def fetchGeomMeanLongSunDegrees(julianCentury):
    geomMeanLongSunDegrees =  (280.46646 + julianCentury * (36000.76983 + julianCentury * 0.0003032)) % 360
    return geomMeanLongSunDegrees

def fetchJulianCentury(dateObj):
    initialDate = datetime.datetime.strptime('1899, 12, 30', "%Y, %m, %d")
    finalDate = dateObj
    numericalDate = (finalDate - initialDate).days    
    julianDay = numericalDate + 2415018.5 + TIMEPASTLOCALMIDNIGHT - TIMEZONE / 24
    julianCentury = (julianDay - 2451545) / 36525
    return julianCentury

def fetchObliqCorrDegrees(julianCentury):
    meanObliqEclipticDegrees = 23 + (26 + ((21.448 - julianCentury * (46.815 + julianCentury * (0.00059 - julianCentury * 0.001813)))) / 60) / 60    
    obliqCorrDegrees = meanObliqEclipticDegrees + 0.00256 * cos(radians(125.04 - 1934.136 * julianCentury))
    return obliqCorrDegrees

def fetchNextEvent(zipcode):
    today = loadToday()
    events = {
        "dawn-today": fetchDawn(zipcode, False, False),
        "noon-today": fetchSolarNoon(zipcode, False, False),
        "dusk-today": fetchDusk(zipcode, False, False),
        "dawn-tomorrow": fetchDawn(zipcode, True, False)
    }
    diffEvents = {}
    txtStr = ""
    closestTime = None
    closestEvent = ""
    for id, (when, time) in enumerate(events.items()):
        diff = floor(fetchDiff(time, True) * TOMETRIC)
        if diff > 0 and (closestTime == None or diff < closestTime  ):
            closestEvent = when
            closestTime = diff
    nextEventTime = today['seconds'] + closestTime
    if nextEventTime > 100000:
        nextEventTime -= 100000
    return closestEvent.split('-')[0] + " " + format(nextEventTime, ",") + " [" + format(closestTime, ",") + "]"
            
            
def fetchSolarNoon(zipcode, tomorrow, asNumber):

    coords = fetchCoords(zipcode)
    if coords == None:
        return False
    
    latitude = coords['latitude']
    longitude = coords['longitude']
    dateObj = datetime.datetime.today()
    if (tomorrow):
        dateObj = datetime.datetime.today() + datetime.timedelta(days=1) 
    julianCentury = fetchJulianCentury(dateObj)


    obliqCorrDegrees = fetchObliqCorrDegrees(julianCentury)
    varY = tan(radians(obliqCorrDegrees / 2)) * tan(radians(obliqCorrDegrees / 2))
    eccentEarthOrbit = 0.016708634 - julianCentury * (0.000042037 + 0.0000001267 * julianCentury)
    geomMeanLongSunDegrees = fetchGeomMeanLongSunDegrees(julianCentury)
    geomMeanAnomSunDegrees = fetchGeomMeanAnomSunDegrees(julianCentury)
    eqOfTime = 4 * degrees(varY * sin(2*radians(geomMeanLongSunDegrees))
        - 2 * eccentEarthOrbit * sin(radians(geomMeanAnomSunDegrees))
        + 4 * eccentEarthOrbit * varY * sin(radians(geomMeanAnomSunDegrees))
        * cos(2 * radians(geomMeanLongSunDegrees)) - 0.5* varY * varY
        * sin(4 * radians(geomMeanLongSunDegrees)) - 1.25 * eccentEarthOrbit * eccentEarthOrbit
        * sin(2 * radians(geomMeanAnomSunDegrees)))
    solarNoonCent = (720 - 4 * longitude - eqOfTime + TIMEZONE * 60) / 1440
    if (asNumber):
        return solarNoonCent
    seconds = floor(SECONDSINDAY * solarNoonCent)
    timeStr = formatTime(seconds)
    if (False):
        print('numericalDate:', numericalDate, 'julian day:', julianDay, 
              'julian century:', julianCentury, 'mean oblique ecliptic degrees:', meanObliqEclipticDegrees, 
              'obliq corr degrees:', obliqCorrDegrees, 'varY:', varY, 
              'eccent earth orbit:', eccentEarthOrbit, 'geo mean long sun degrees:', geomMeanLongSunDegrees, 
              'geo mean anom sun degrees:', geomMeanAnomSunDegrees, 
              'eq of time:', eqOfTime, 'solar noon cent:', solarNoonCent)
    
    return dateObj.strftime("%Y/%m/%d") + " " + timeStr




def formatTime(seconds):
    minutes = floor (seconds / 60)
    seconds %= 60
    hours = floor(minutes / 60)
    minutes %= 60
    hoursString = str(hours)
    if (hours < 10):
        hoursString = "0" + hoursString
    minutesString = str(minutes)
    if (minutes < 10):
        minutesString = "0" + minutesString
    secondsString = str(seconds)
    if (seconds < 10):
        secondsString = "0" + secondsString

    return hoursString + ":" + minutesString + ":" + secondsString