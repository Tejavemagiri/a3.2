#!/usr/bin/python3
import sys, time
from easysnmp import Session
from easysnmp import snmp_get
import math
import easysnmp
information = sys.argv[1]
arguments = information.split(':')
ipAddress = arguments[0]
port = arguments[1]
community = arguments[2]
sampleFreq = float(sys.argv[2])
sampleTime = 1/sampleFreq
samples = int(sys.argv[3])
sample2 = []
ID = []
sampletimeA = []
sample1 = []
for i in range(1,samples):
sampletimeA = i * sampleTime
for i in range(4, len(sys.argv)):
ID.append(sys.argv[i])
ID.insert(0,'1.3.6.1.2.1.1.3.0')
def oidRate():
global sample1, samplingTime, sampleNumber, samples, loop
snmpSession=Session(hostname=ipAddress,remote_port=port,community=co
mmunity,version=2,timeout=1,retries=1).get(ID)
sampledTime = int(snmpSession[0].value)*0.01
sample2 = []
for i in range(1,len(snmpSession)):
if snmpSession[i].value!='NOSUCHOBJECT' and 
snmpSession[i].value!='NOSUCHINSTANCE' and 
snmpSession[i].value!='INVALID':
sample2.append(int(snmpSession[i].value))
if sampleNumber!=0 and len(sample1)>0 :
difference = sample2[i-1] - sample1[i1]
timeDifference = sampledTime - 
samplingTime
RateOID = difference/timeDifference
if difference < 0:
if snmpSession[i].snmp_type 
== 'COUNTER32' and timeDifference > 0:
difference = 
difference + (2**32)
if i == 1:
print(str(s_t) + "|" ,end='')
h = 
round((difference / timeDifference))
print(str(h) + "|" ,end='')
else:
h = 
round((difference / timeDifference))
print(str(h) + "|")
elif 
snmpSession[i].snmp_type =='COUNTER64' and timeDifference > 0:
difference = 
difference + (2**64)
if i == 1:
print(str(s_t) + "|" ,end='')
h = 
round((difference / timeDifference))
print(str(h) + "|" ,end='')
else:
h = 
round((difference / timeDifference))
print(str(h) + "|" ,end='')
elif timeDifference > 0 :
if i == 1:
print(str(s_t) + 
"|" ,end='')
h = 
round((difference / timeDifference))
print(str(h) + 
"|" ,end='')
else:
h = 
round((difference / timeDifference))
print(str(h) + 
"|" ,end='')
elif timeDifference < 0:
if i == 1:
sample2 = []
sample1 = []
loop = range(0, 
samples+1+2)
print(str(s_t) + 
"|" ,end='')
print("agent 
restarted"+ "|")
else:
sample2 = []
sample1 = []
loop = range(0, 
samples+1+2)
print("Agent 
Restarted"+ "|")
break
if sampleNumber != 0 and len(sample1)>0:
print()
samplingTime = sampledTime
sample1 = sample2
if samples == -1:
sampleNumber = 0
sample1 = []
while 1:
s_t = (time.time())
oidRate()
r_t=(time.time())
sampleNumber = sampleNumber +1
if r_t-s_t > sampleTime:
time.sleep(sampleTime-abs(sampleTime - 
r_t+s_t))
else:
time.sleep(abs(sampleTime - r_t+s_t))
else:
sample1 = []
loop = range(0,samples+1)
for sampleNumber in loop:
s_t = (time.time())
oidRate()
r_t = (time.time())
if r_t-s_t > sampleTime:
time.sleep(sampleTime-abs(sampleTime - 
r_t+s_t))
else:
time.sleep(abs(sampleTime - r_t+s_t)
