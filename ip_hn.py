import csv
def parse_hn():
	f = open ('routers.txt')
	ip_book = {}
	ips = []
	hostnames = []
	for line in f:
		index = line.find(',')
		ip = line[:index]
		hostname = line[index+1:]
		print(ip)
		print(hostname)
		ip_book[ip] = hostname.rstrip()
		ips.append(ip)
		hostnames.append(hostname.rstrip())
		#generate_csv(ip_book)
	return ip_book, hostnames, ips

def generate_csv(ip_book):
	with open('test.csv', 'w') as f:
	    fieldnames = ['IP', 'HOSTNAME']
	    writer = csv.DictWriter(f, fieldnames=fieldnames)
	    writer.writeheader()
	    data = [dict(zip(fieldnames, [k, v])) for k, v in ip_book.items()]
	    writer.writerows(data)

def main():
	ip_book,hostnames, ips = parse_hn()
	print(ip_book)
	print(hostnames)
	print(ips)
	generate_csv(ip_book)


if __name__ == '__main__':
	main()