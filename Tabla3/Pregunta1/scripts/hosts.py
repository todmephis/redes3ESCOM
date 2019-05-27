addr_book = {}
def read_hosts():
	index = 0
	hosts = open('/etc/hosts','r')
	#out = open("../outputs/routers.txt","w+")
	for line in hosts:
		host = line.split()[1:]
		print(type(host))
		addr = line.split()[:1]
		try:
			addr_book[host.pop()] = addr.pop()
		except:
			break
	print(addr_book)
	"""
	index = index + 1
	sel = 'R'+str(index)+''
	print(sel)
	out.write(addr_book[sel])
	"""

def main():
	read_hosts()

if __name__ == '__main__':
	main()