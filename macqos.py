#!/usr/bin/env python

##############################################################################
# Imports below
##############################################################################
from pprint import pprint
from pprint import pformat

import datetime
import io
import time
import json
import requests
import sys
import os

# Disable Certificate warning
try:
  requests.packages.urllib3.disable_warnings()
except:
  pass

reload(sys)
sys.setdefaultencoding('utf-8')


##############################################################################
# Variables below
##############################################################################


APIC_IP = '10.153.0.115'
APIC_BASE = 'https://%s/api/v1' % APIC_IP
APIC_LOGIN = 'admin'
APIC_PASSWD = 'C1sc0123'

os.environ['no_proxy'] = '%s' % APIC_IP

##############################################################################
# Start API Session APIC_EM
##############################################################################

apic_credentials = json.dumps({'username':APIC_LOGIN,'password':APIC_PASSWD})
tmp_headers = {'Content-type': 'application/json'}
tmp_get = '%s/ticket' % APIC_BASE
print("Connecting to APIC-EM ..."+'\r\n')
req = requests.post(tmp_get, data=apic_credentials, verify=False, headers=tmp_headers)

# Add session ticket to my http header for subsequent calls
apic_session_ticket = req.json()['response']['serviceTicket']
apic_headers = {'Content-type': 'application/json', 'X-Auth-Token': apic_session_ticket}
print("Connecting to APIC-EM Done" +'\r\n')

	
##############################################################################
# Get a Host Inventory (Mac Address + IP address)
##############################################################################
def gethostinventory():
	#global host_list
	url = '%s/host' % APIC_BASE
	req_inv = requests.get(url,verify=False, headers=apic_headers)
	parsed_result= req_inv.json()
	req_list=parsed_result['response']
	
	host_list = []
	i = 0
	
	for item in req_list:
		i = i + 1
		host_list.append([i,str(item["hostMac"]),str(item["hostIp"])])
	return host_list;

##############################################################################
# Prioritize and IP
##############################################################################

def prioritizeIp(Ip):
	url = '%s/policy/flow' % APIC_BASE
	payload = {"flowType": "VIDEO", "sourceIP": Ip}
	r = requests.post(url, data=json.dumps(payload), verify=False, headers=apic_headers)


##############################################################################
# Core Program
##############################################################################

os.system('cls' if os.name == 'nt' else 'clear')
hostinventory = gethostinventory()

for host in hostinventory:
  print host

number = input ("\n\nPlease select the host you want to prioritize\n\n")

host_mac = hostinventory [number-1][1]
host_ip = hostinventory [number-1][2]


print "\n\nYou have chosen Host MAC address:\n"
print host_mac
print "\n\nYou have chosen Host IP address:\n"
print host_ip

prioritizeIp(host_ip)
