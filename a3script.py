#!/usr/bin/python3
import sys
import time
from easysnmp import Session
if len(sys.argv) < 2:
    print("Insufficient command-line arguments. Usage: python3 script.py <information>")
    sys.exit(1)

# Retrieve command-line arguments
information = sys.argv[1]
arguments = information.split(':')
ipAddress = arguments[0]
port = arguments[1]
community = arguments[2]
sampleFreq = float(sys.argv[2])
sampleTime = 1 / sampleFreq
samples = int(sys.argv[3])

sample2 = []
ID = []
sampletimeA = []
sample1 = []

# Parse arguments and create ID list
for i in range(1, samples):
    sampletimeA = i * sampleTime

for i in range(4, len(sys.argv)):
    ID.append(sys.argv[i])
ID.insert(0, '1.3.6.1.2.1.1.3.0')

def oidRate():
    global sample1, samplingTime, sampleNumber, samples, loop
    snmpSession = Session(
        hostname=ipAddress,
        remote_port=port,
        community=community,
        version=2,
        timeout=1,
        retries=1
    ).get(ID)
    sampledTime = int(snmpSession[0].value) * 0.01
    sample2 = []

    for i in range(1, len(snmpSession)):
        if (
            snmpSession[i].value != 'NOSUCHOBJECT' and
            snmpSession[i].value != 'NOSUCHINSTANCE' and
            snmpSession[i].value != 'INVALID'
        ):
            sample2.append(int(snmpSession[i].value))
            if sampleNumber != 0 and len(sample1) > 0:
                difference = sample2[i - 1] - sample1[i - 1]
                timeDifference = sampledTime - samplingTime

                # Handle relative change for GAUGE type values
                if snmpSession[i].snmp_type == 'GAUGE' and timeDifference > 0:
                    relativeChange = difference - sample1[i - 1]
                    if i == 1:
                        print(str(s_t) + "|" ,end='')
                        h = round((difference / timeDifference))
                        print(str(h) + "|" ,end='')
                    else:
                        h = round((difference / timeDifference))
                        print(str(h) + " (+" + str(relativeChange) + ")|" ,end='')

                # Handle COUNTER32 and COUNTER64 values as before
                elif snmpSession[i].snmp_type == 'COUNTER32' and timeDifference > 0:
                    if difference < 0:
                        difference = difference + (2 ** 32)
                    if i == 1:
                        print(str(s_t) + "|" ,end='')
                        h = round((difference / timeDifference))
                        print(str(h) + "|" ,end='')
                    else:
                        h = round((difference / timeDifference))
                        print(str(h) + "|" ,end='')

                elif snmpSession[i].snmp_type == 'COUNTER64' and timeDifference > 0:
                    if difference < 0:
                        difference = difference + (2 ** 64)
                    if i == 1:
                        print(str(s_t) + "|" ,end='')
                        h = round((difference / timeDifference))
                        print(str(h) + "|" ,end='')
                    else:
                        h = round((difference / timeDifference))
                        print(str(h) + "|" ,end='')

                elif timeDifference > 0:
                    if i == 1:
                        print(str(s_t) + "|" ,end='')
                        h = round((difference / timeDifference))
                        print(str(h) + "|")
