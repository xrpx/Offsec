#!/usr/bin/env python3

# Author:		xrpx
# Description:		Input full or partial target name to get ARIN registered ranges
# Last modified: 	May 31, 2019
# Dependencies:     <nil>
# Usage:        > 'python3 fingerprintMe.py' and 'Enter the search term: ' for target search

import requests, time, csv, os
import subprocess,re, json

# Set unique filename for each run
timestamp = str(time.time())
filename = 'arin_' + timestamp + '.csv'

def write_csv(dictRow,filename):
    # Export data as csv
    
    if os.path.exists(filename):
        # Append if file exists
        append_write = 'a'

        with open(filename, append_write) as f:
            w = csv.DictWriter(f, ['Start IP', 'End IP', 'CIDR'], extrasaction='ignore')
            w.writerow(dictRow)

    else:
        # Or create new file with headers
        append_write = 'w'
    
        with open(filename, append_write) as f:
            w = csv.DictWriter(f, ['Start IP', 'End IP', 'CIDR'], extrasaction='ignore')
            w.writeheader()
            w.writerow(dictRow)
    
# Accept user input and query ARIN WHOIS
search_term = input('Enter the search term: ')
full_whois = subprocess.getoutput('whois -h whois.arin.net "z %s"' % search_term)

# Retrieve identified networks. In furture, this should query identified orgs and contacts for any linked networks.
my_nets = re.findall('\(NET-(.*?)\)', full_whois)

for nets in my_nets:
    f = requests.get('https://whois.arin.net/rest/net/NET-%s.json' % nets)
    full_json = f.text
    d = json.loads(full_json)
    cidrLength = d['net']['netBlocks']['netBlock']['cidrLength']['$']
    startAddress = d['net']['netBlocks']['netBlock']['startAddress']['$'] 
    endAddress = d['net']['netBlocks']['netBlock']['endAddress']['$']

    dictRow = {'Start IP': startAddress, 'End IP': endAddress, 'CIDR': startAddress + '/' + cidrLength}
    write_csv(dictRow, filename)
