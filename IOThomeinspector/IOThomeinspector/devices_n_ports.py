"""Scan a network range for connected devices and ports."""
import nmap
import socket
from pprint import pprint
nm = nmap.PortScanner()
ip_addresses = []
scans = []
this_local_ip = socket.gethostbyname(socket.gethostname())
test_ip = this_local_ip.split('.')
for index_one in range(16,32):
    test_ip[1] = str(index_one)
    for index_two in range(256):
        test_ip[2] = str(index_two)
        test_ip[3] = '0'
        ip_addresses.append('.'.join(test_ip))
for ip in ip_addresses:
    scans.append(nm.scan(ip + '/24', '23, 9100', '--stats-every 2s'))

# print(the_scan['scan'][this_local_ip]['tcp'][port]['version'])
# print(the_scan['scan'][this_local_ip]['tcp'][port]['product'])
# print(the_scan['scan'][this_local_ip]['tcp'][port]['state'])

for scan in scans:    
    for i in the_scan['scan']:
        for x in the_scan['scan'][i]['tcp']:
            if the_scan['scan'][i]['tcp'][x]['state'] == 'open':
                pprint(scan)
                pprint(the_scan['scan'][i]['tcp'][x]['version'])
                pprint(the_scan['scan'][i]['tcp'][x]['product'])
                pprint(the_scan['scan'][i]['tcp'][x]['state'])
                print('------------------')

