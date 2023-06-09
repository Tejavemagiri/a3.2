#!/usr/bin/python3

import sys
import time
from easysnmp import Session

information = sys.argv[1]
arguments = information.split(':')
ipAddress = arguments[0]
port = arguments[1]
community = arguments[2]
sampleFreq = float(sys.argv[2])
sampleTime = 1/sampleFreq
samples = int(sys.argv[3])

counterOids = []
gaugeOids = []

for i in range(4, len(sys.argv)):
    if sys.argv[i].startswith('1.3.6.1.4.1.4171.40'):
        counterOids.append(sys.argv[i])
    elif sys.argv[i].startswith('1.3.6.1.4.1.4171.60'):
        gaugeOids.append(sys.argv[i])

oidList = ['1.3.6.1.2.1.1.3.0'] + counterOids + gaugeOids

sample1 = []
previousTime = 0

def handle_counter32(counter):
    if counter < 0:
        counter += 2 ** 32
    return counter

def handle_counter64(counter):
    if counter < 0:
        counter += 2 ** 64
    return counter

def calculate_rate(value, previous_value, time_difference):
    rate = (value - previous_value) / time_difference
    return round(rate, 2)

def easysnmp_prober():
    global sample1, previousTime
    session = Session(hostname=ipAddress, remote_port=port, community=community, version=2, timeout=1, retries=1)
    response = session.get(oidList)

    currentTime = int(response[0].value) * 0.01
    sample2 = []

    for i in range(1, len(response)):
        oid_value = response[i].value
        if oid_value != 'NOSUCHOBJECT' and oid_value != 'NOSUCHINSTANCE' and oid_value != 'INVALID':
            sample2.append(int(oid_value))

    if previousTime != 0 and len(sample1) > 0:
        timeDifference = currentTime - previousTime

        counterIndex = 0
        gaugeIndex = 0

        for i in range(1, len(response)):
            current_value = sample2[i-1]
            previous_value = sample1[i-1]

            if response[i].snmp_type == 'COUNTER32':
                current_value = handle_counter32(current_value)
                previous_value = handle_counter32(previous_value)
                rate = calculate_rate(current_value, previous_value, timeDifference)
                print(f"{currentTime} | Counter{counterIndex}: {rate}")
                counterIndex += 1

            elif response[i].snmp_type == 'COUNTER64':
                current_value = handle_counter64(current_value)
                previous_value = handle_counter64(previous_value)
                rate = calculate_rate(current_value, previous_value, timeDifference)
                print(f"{currentTime} | Counter{counterIndex}: {rate}")
                counterIndex += 1

            elif response[i].snmp_type == 'GAUGE':
                change = current_value - previous_value
                print(f"{currentTime} | Gauge{gaugeIndex}: {current_value} (+{change})")
                gaugeIndex += 1

    sample1 = sample2
    previousTime = currentTime

if samples == -1:
    sample1 = []
    while True:
        easysnmp_prober()
        time.sleep(sampleTime)
else:
    sample1 = []
    for _ in range(samples):
        easysnmp_prober()
        time.sleep(sampleTime)
