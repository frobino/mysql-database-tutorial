import os
import time
import datetime
import glob
# import MySQLdb
from time import strftime
 
# os.system('modprobe w1-gpio')
# os.system('modprobe w1-therm')

# cat /sys/class/thermal/thermal_zone*/temp
# cat /sys/class/thermal/thermal_zone0/temp
temp_sensor = '/sys/class/thermal/thermal_zone0/temp'
# cat /proc/cpuinfo
cpu_info = '/proc/cpuinfo'
 
# Variables for MySQL
# db = MySQLdb.connect(host="localhost", user="root",passwd="password", db="temp_database")
# cur = db.cursor()
 
def tempRead():
    t = open(temp_sensor, 'r')
    lines = t.readlines()
    t.close()
 
    temp_string = lines[0]
    temp_c = float(temp_string)/1000.0
    return round(temp_c,1)

def freqRead():
    t = open(cpu_info, 'r')
    lines = t.readlines()
    t.close()

    # cpu Mhz expected to be found at line 7
    cpu0freq_output = lines[7].find('cpu MHz')
    if cpu0freq_output != -1:
        cpu0freq_string = lines[7].strip()[cpu0freq_output+11:]
        cpu0freq_c = float(cpu0freq_string)
    return round(cpu0freq_c,1)

while True:
    temp = tempRead()
    print temp
    freq = freqRead()
    print freq
#     datetimeWrite = (time.strftime("%Y-%m-%d ") + time.strftime("%H:%M:%S"))
#     print datetimeWrite
#     sql = ("""INSERT INTO tempLog (datetime,temperature) VALUES (%s,%s)""",(datetimeWrite,temp))
#     try:
#         print "Writing to database..."
#         # Execute the SQL command
#         cur.execute(*sql)
#         # Commit your changes in the database
#         db.commit()
#         print "Write Complete"
#  
#     except:
#         # Rollback in case there is any error
#         db.rollback()
#         print "Failed writing to database"
#  
#     cur.close()
#     db.close()
    break
