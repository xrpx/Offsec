# Offsec

A collection of scripts for penetration testing.

**reconIP.py**: Shodan lookup script. This reads subnets from a file and queries shodan.io for identified IP address with their hostnames and open ports. You will need an API key from shodan.io to run this script.

Syntax:
    # python3 reconIP.py ip.txt
where ip.txt contains in-scope subnets in CIDR format separated by newline. Following dependencies should be met:
    # pip3 install shodan, netaddr

The script will store output in a CSV file with filename *shodan_results_timestamp.csv

**aws_mfa.sh**: Bash wrapper to query AWS using MFA token. Useful to interact with cloud environment if token is obtained.

Syntax:
    # /bin/bash aws_mfa.sh
Dependencies:
    # pip3 install awscli