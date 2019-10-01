#!/usr/bin/python
import sys
import json
from datetime import datetime
import os

#adapted from the original source at: http://www.desert-home.com/2014/12/acurite-weather-station-raspberry-pi_3.html

#returns date as a string in the format d-m-y
def getDateStr(day,month,year):
    return str(day)+'-'+str(month)+'-'+str(year)

#current date and time
t = datetime.now()
#current date, the date the data file was created
data_date = getDateStr(t.day,t.month,t.year)
buff = ''

while True:    
    try:
        #update current date and time
        t = datetime.now()
        #update current time, get in a string
        date = getDateStr(t.day,t.month,t.year)
        #set filepath to most current data file to be edited
        filepath = '/home/pi/Desktop/Data/'+data_date+'.csv'

        #if the date that the data was created isn't the same as the current date,
        if data_date != date:
            #update date for data file
            data_date = getDateStr(t.day,t.month,t.year)
        
        buff += sys.stdin.read(1)
        if buff.endswith('\n'):
            #get the new data
            data = json.loads(buff[:-1])

            #if it already exists, open the file for the day
            if os.path.exists(filepath):
                f = open(filepath, 'a')
            else:
                #if it doesn't already exist, make a new one
                f = open(filepath, 'w')
                os.chown(filepath, 1000, -1)
                f.write('date,time,wind speed,wind direction,temperature,humidity,rain counter\n')
                f.close()
                
                f = open(filepath, 'a')

            #append data at the end
            f.write(date+','+str(t.hour)+':'+str(t.minute)+':'+str(t.second)+','+str(data['windSpeed']['WS'])+','+str(data['windDirection']['WD'])+','+str(data['temperature']['T'])+','+str(data['humidity']['H'])+','+str(data['rainCounter']['RC']+'\n'))
            #close the file
            f.close()

            #shut it down
            sys.stdout.flush()
            buff = ''
            
    except KeyboardInterrupt:
        #shut it down
        sys.stdout.flush()
        sys.exit()
