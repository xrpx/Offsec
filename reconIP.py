#!/usr/bin/env python3

# Author:		xrpx
# Description:		Passive scan IP address/ range using shodan.io
# Last modified: 	May 31, 2019
# Dependencies:     pip3 install shodan, netaddr
# Usage:        > 'python3 reconIP.py filename.txt' where filename.txt contains CIDR formatted subnets to scan

import shodan, sys, csv, os, time
from netaddr import IPAddress, IPNetwork

# Initiate session with API key
########## CONFIGURATION ZONE ###########
api_key='YOUR_API_KEY_HERE'
#########################################
api = shodan.Shodan(api_key)

# Generate filename before entering loop
timestamp = str(time.time())
filename = 'shodan_results_' + timestamp + '.csv'


def write_csv(ipinfo,filename):
    # Export data as csv
    if os.path.exists(filename):
        # Append if file exists
        append_write = 'a'

        with open(filename, append_write) as f:
            w = csv.DictWriter(f, ['ip_str', 'hostnames', 'ports'], extrasaction='ignore')
            w.writerow(ipinfo)

    else:
        # Or create new file with headers
        append_write = 'w'
    
        with open(filename, append_write) as f:
            w = csv.DictWriter(f, ['ip_str', 'hostnames', 'ports'], extrasaction='ignore')
            w.writeheader()
            w.writerow(ipinfo)

def lookups(ip, filename):
    try:
    
        for ipn in ip:
        
            ip_str = [str(ipn)]

# Continue execution upon 'IP not found' exception
            try:
                ipinfo = api.host(ip_str)
                write_csv(ipinfo, filename)

            except shodan.APIError:
                pass

    except Exception as e:
            print('Error: {}'.format(e))
# Uncomment to debug
#            print('Error! Code: {c}, Message, {m}'.format(c = type(e).__name__, m = str(e)))
        

##### MAIN #####

with open(sys.argv[1]) as nets:
    for subnet in nets:
        ip = IPNetwork(subnet)
        lookups(ip, filename)

