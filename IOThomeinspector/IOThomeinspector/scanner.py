import subprocess


def find_local_ip_and_mask():
	local_ip = ''
	mask = ''
	net_info = str(subprocess.Popen('ifconfig', stdout=subprocess.PIPE).communicate()[0])
	net_info_list = net_info.split(' ')
	for i in net_info_list:
		if 'Bcast' in i:
			local_ip = net_info_list[net_info_list.index(i) - 2].split(':')[1]	
			mask = net_info_list[net_info_list.index(i) + 2].split(':')[1]
			mask = mask[:-1]
			print(mask)
	return (local_ip, mask)


def find_ip_range(ip_mask):
	section_range = []
	min_ip = []
	max_ip = []
	base_ip = ip_mask[0].split('.')
	mask_sections = [section for section in ip_mask[1].split('.')]
	for i in mask_sections:
		section_range.append(255 - int(i))
	for x in range(len(section_range)):
		if section_range[x] == 0:
			min_ip.append(str(base_ip[x]))
			max_ip.append((base_ip[x]))
		else:
			min_ip.append('0')
			max_ip.append(str(section_range[x]))
	return (min_ip, max_ip)


def scan_ip_range(min_max):
	scans = []
	min_ip = min_max[0]
	max_ip = min_max[1]
	scan_ip = ['172.16.11.242', '172.16.0.101']
	for ip in scan_ip:
		scan = subprocess.Popen(['sudo', 'nmap', '-O', '-T5', '--top-ports', '25', ip], stdout=subprocess.PIPE).communicate()[0]
		if 'open' in scan or 'filtered' in scan:
			scans.append(scan)
	return scans


def get_warning(scans):
	port_status = []
	for scan in scans:
		for element in scan.split('\n'):
			if 'telnet' in element:
				element_list = element.split(' ')
				element_list = [i for i in element_list if i != '']	
				port_status.append(element_list[element_list.index('telnet') - 1])
	return port_status


def main():
	a = find_local_ip_and_mask()
	b = find_ip_range(a)
	c = scan_ip_range(b)
	d = get_warning(c)
	return d
