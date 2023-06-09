#!/usr/bin/python

import sys
import time
from easysnmp import Session

information = sys.argv[1]
arguments = information.split(':')
ipAddress = arguments[0]
port = arguments[1]
community = arguments[2]
sampleFreq = float(sys.argv[2])
sampleTime = 1 / sampleFreq
samples = int(sys.argv[3])
oidCounters = []
oidGauges = []

for i in range(4, len(sys.argv)):
    if sys.argv[i].startswith('1.3.6.1.4.1.4171.40.'):
        oidCounters.append(sys.argv[i])
    elif sys.argv[i].startswith('1.3.6.1.4.1.4171.60.'):
        oidGauges.append(sys.argv[i])

oidCounters.insert(0, '1.3.6.1.2.1.1.3.0')
oidGauges.insert(0, '1.3.6.1.2.1.1.3.0')

def calculate_rate(previous, current, time_diff):
    if current < previous:
        if current < 0:
            current += 2 ** 32
        rate = (current - previous) / time_diff
        return rate
    else:
        return (current - previous) / time_diff

def probe_oids(oids):
    session = Session(hostname=ipAddress, remote_port=port, community=community, version=2, timeout=1, retries=1)
    response = session.get(oids)
    return [int(oid.value) if oid.value not in ('NOSUCHOBJECT', 'NOSUCHINSTANCE') else -1 for oid in response]

def print_output(time, counters, gauges):
    output = str(time) + " | "
    for counter in counters:
        output += str(round(counter)) + " | "
    for i, gauge in enumerate(gauges):
        output += str(round(gauge))
        if i != len(gauges) - 1:
            output += " | "
    print(output)

counters_prev = probe_oids(oidCounters)
gauges_prev = probe_oids(oidGauges)

if samples == -1:
    while True:
        time.sleep(sampleTime)
        counters_curr = probe_oids(oidCounters)
        gauges_curr = probe_oids(oidGauges)
        current_time = int(time.time())

        time_diff = current_time - counters_prev[0]
        counters_rate = [calculate_rate(counters_prev[i], counters_curr[i], time_diff) for i in range(len(counters_curr))]
        gauges_change = [gauges_curr[i] - gauges_prev[i] for i in range(len(gauges_curr))]

        print_output(current_time, counters_rate, gauges_change)

        counters_prev = counters_curr
        gauges_prev = gauges_curr

else:
    for _ in range(samples):
        time.sleep(sampleTime)
        counters_curr = probe_oids(oidCounters)
        gauges_curr = probe_oids(oidGauges)
        current_time = int(time.time())

        time_diff = current_time - counters_prev[0]
        counters_rate = [calculate_rate(counters_prev[i], counters_curr[i], time_diff) for i in range(len(counters_curr))]
        gauges_change = [gauges_curr[i] - gauges_prev[i] for i in range(len(gauges_curr))]

        print_output(current_time, counters_rate, gauges_change)

        counters_prev = counters_curr
        gauges_prev = gauges_curr

