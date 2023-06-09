#!/usr/bin/python

import sys
import time
import easysnmp
from easysnmp import Session

# Extract information from command line
info_agent = sys.argv[1]
b = info_agent.split(':')
agent_ip_addr = b[0]
agent_port = b[1]
agent_community = b[2]
sample_frequency = float(sys.argv[2])
samples = int(sys.argv[3])
sample_time = 1 / sample_frequency

oids = []
current_oid = []
previous_oid = []

# Store the provided OIDs
for number_oids in range(4, len(sys.argv)):
    oids.append(sys.argv[number_oids])
oids.insert(0, '1.3.6.1.2.1.1.3.0')

def easysnmp_prober():
    global current_oid, current_time
    session = Session(hostname=agent_ip_addr, remote_port=agent_port, community='public', version=2, timeout=1, retries=1)
    try:
        response = session.get(oids)
    except easysnmp.EasySNMPTimeoutError:
        print("Error: Connection timed out while retrieving SNMP data. Please check the SNMP agent and network connectivity.")
        sys.exit(1)

    previous_oid = []
    for get_oids in range(1, len(response)):
        if response[get_oids].value != 'NOSUCHOBJECT' and response[get_oids].value != 'NOSUCHINSTANCE':
            previous_oid.append(int(response[get_oids].value))

            if count != 0 and len(current_oid) > 0:
                oid_diff = int(previous_oid[get_oids - 1]) - int(current_oid[get_oids - 1])
                time_diff = round(previous_time - current_time, 1)
                rate = int(oid_diff / time_diff)
                if rate < 0:
                    if response[get_oids].snmp_type == 'COUNTER32':
                        oid_diff = oid_diff + 2 ** 32
                        print(str(previous_time) + "|" + str(oid_diff / time_diff) + "|" + "|" + "|" + "|")
                    elif response[get_oids].snmp_type == 'COUNTER64':
                        oid_diff = oid_diff + 2 ** 64
                        print(str(previous_time) + "|" + str(oid_diff / time_diff) + "|" + "|" + "|" + "|")
                else:
                    print(str(previous_time) + "|" + str(rate) + "|" + "|" + "|" + "|")

    current_oid = previous_oid
    current_time = previous_time

if samples == -1:
    count = 0
    current_oid = []
    while True:
        previous_time = time.time()
        easysnmp_prober()
        response_time = time.time()
        count = count + 1
        time.sleep(abs(sample_time - response_time + previous_time))
else:
    current_oid = []
    for count in range(0, samples + 1):
        previous_time = time.time()
        easysnmp_prober()
        response_time = time.time()
        time.sleep(abs(sample_time - response_time + previous_time))
