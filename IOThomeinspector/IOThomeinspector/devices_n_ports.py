"""Scan a network range for connected devices and ports."""
import nmap
import socket
from pprint import pprint
nm = nmap.PortScanner()
this_local_ip = socket.gethostbyname(socket.gethostname())
this_local_ip = this_local_ip.split('.')
this_local_ip[2] = '0'
this_local_ip[3] = '0'
this_local_ip = ".".join(this_local_ip)
this_local_ip += '/24'
the_scan = nm.scan(this_local_ip, '23, 9100')
pprint(the_scan)

print(the_scan['scan'][this_local_ip]['tcp'][port]['version'])
print(the_scan['scan'][this_local_ip]['tcp'][port]['product'])
print(the_scan['scan'][this_local_ip]['tcp'][port]['state'])

for i in the_scan['scan']:
    for x in the_scan['scan'][i]['tcp']:
        pprint(the_scan['scan'][i]['tcp'][x]['version'])
        pprint(the_scan['scan'][i]['tcp'][x]['product'])
        pprint(the_scan['scan'][i]['tcp'][x]['state'])

