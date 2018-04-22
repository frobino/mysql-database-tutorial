# Requires MySQLdb package installed:
#
#   sudo apt-get install libmariadbclient-dev
#   pip install mysqlclient
#
# Requires a mysql db on place:
#
#   sudo mysql -u -p
#   CREATE DATABASE temp_database;
#   SHOW DATABASES;
#   USE mydatabase2;
#   CREATE TABLE tempLog0(datetime DATETIME NOT NULL, temperature FLOAT(5,2) NOT NULL);
#   CREATE TABLE tempLog1(datetime DATETIME NOT NULL, temperature FLOAT(5,2) NOT NULL);
#   CREATE TABLE freqLog0(datetime DATETIME NOT NULL, temperature FLOAT(6,2) NOT NULL);
#   CREATE TABLE freqLog1(datetime DATETIME NOT NULL, temperature FLOAT(6,2) NOT NULL);
#   DESCRIBE tempLog0;
#
# Grafana graph configuration
#  SELECT
#   UNIX_TIMESTAMP(datetime) as time_sec,
#   frequency as value,
#   'freqCore0' as metric
#  FROM freqLog0
# WHERE $__timeFilter(datetime)
# ORDER BY datetime ASC

import time
import datetime
import glob
import MySQLdb
from time import strftime
 
# cat /sys/class/thermal/thermal_zone*/temp
# cat /sys/class/thermal/thermal_zone0/temp
temp0_sensor = '/sys/class/thermal/thermal_zone0/temp'
# cat /sys/class/thermal/thermal_zone0/temp
temp1_sensor = '/sys/class/thermal/thermal_zone1/temp'
# cat /proc/cpuinfo
cpu_info = '/proc/cpuinfo'

# Variables for MySQL access
db = MySQLdb.connect(host="localhost", user="grafanaReader", passwd="password", db="mydatabase2")
cur = db.cursor()
 
def temp0Read():
    t = open(temp0_sensor, 'r')
    lines = t.readlines()
    t.close()
 
    temp_string = lines[0]
    temp_c = float(temp_string)/1000.0
    return round(temp_c,1)

def temp1Read():
    t = open(temp1_sensor, 'r')
    lines = t.readlines()
    t.close()
 
    temp_string = lines[0]
    temp_c = float(temp_string)/1000.0
    return round(temp_c,1)

def freq0Read():
    t = open(cpu_info, 'r')
    lines = t.readlines()
    t.close()

    # cpu 0 Mhz expected to be found at line 7
    cpu0freq_output = lines[7].find('cpu MHz')
    if cpu0freq_output != -1:
        cpu0freq_string = lines[7].strip()[cpu0freq_output+11:]
        cpu0freq_c = float(cpu0freq_string)
    return round(cpu0freq_c,1)

def freq1Read():
    t = open(cpu_info, 'r')
    lines = t.readlines()
    t.close()

    # cpu 1 Mhz expected to be found at line 34
    cpu1freq_output = lines[34].find('cpu MHz')
    if cpu1freq_output != -1:
        cpu1freq_string = lines[34].strip()[cpu1freq_output+11:]
        cpu1freq_c = float(cpu1freq_string)
    return round(cpu1freq_c,1)


while True:
    temp0 = temp0Read()
    print temp0
    temp1 = temp1Read()
    print temp1
    freq0 = freq0Read()
    print freq0
    freq1 = freq1Read()
    print freq1
    
    datetimeWrite = (time.strftime("%Y-%m-%d ") + time.strftime("%H:%M:%S"))
    print datetimeWrite
    # classic mysql query/command (see mysql-workbench)
    sqlTempLog0 = ("""INSERT INTO tempLog0 (datetime,temperature) VALUES (%s,%s)""",(datetimeWrite,temp0))
    sqlTempLog1 = ("""INSERT INTO tempLog1 (datetime,temperature) VALUES (%s,%s)""",(datetimeWrite,temp1))
    sqlFreqLog0 = ("""INSERT INTO freqLog0 (datetime,frequency) VALUES (%s,%s)""",(datetimeWrite,freq0))
    sqlFreqLog1 = ("""INSERT INTO freqLog1 (datetime,frequency) VALUES (%s,%s)""",(datetimeWrite,freq1))
    try:
        print "Writing to database..."
        # Execute the SQL command
        cur.execute(*sqlTempLog0)
        cur.execute(*sqlTempLog1)
        cur.execute(*sqlFreqLog0)
        cur.execute(*sqlFreqLog1)
        # Commit your changes in the database
        db.commit()
        print "Write Complete"
 
    except:
        # Rollback in case there is any error
        db.rollback()
        print "Failed writing to database"
 
    cur.close()
    db.close()
    break
