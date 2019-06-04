#from pygtail import Pygtail
import sys
import os
import subprocess
import collections
import time
import threading
import sendmail

'''
for line in Pygtail("/var/log/snmp-logs/r16.log"):
	sys.stdout.write(line)
'''
#LOG_FILE = os.path.abspath('/var/log/syslog')
#%SYS-1-CPURISINGTHRESHOLD: Threshold: Total CPU Utilization(Total/Intr): 75%/100%, Top 3 processes(Pid/Util):  91/75%, 2/0%, 51/0%

#LOG_FILE = os.path.abspath('/var/log/snmp-logs/r16.log')
#LOG_FILE = os.path.abspath('/var/log/snmp-logs/r16.log')

WATCH_FOR = [ 	'%LINK-3-UPDOWN ', #interface on/off
				'%LINEPROTO-5-UPDOWN', #line protocol on/off
				'%LINK-5-CHANGED', #LINK STAT CH
				'%SYS-1-CPURISINGTHRESHOLD', #CPU treshold rising
				'%SYS-1-CPUFALLINGTHRESHOLD', #CPU threshold falling
				'%SYS-5-CONFIG_I: Configured from console by console', #configuration
				'%SYS-6-LOGGINGHOST_STARTSTOP: Logging to host 192.168.1.118 port 514 stopped'#logging server
				]

def tail(file, n):

	with open(file, "r") as f:

		f.seek (0, 2)           # Seek @ EOF
		fsize = f.tell()        # Get Size
		f.seek (max (fsize-1024, 0), 0) # Set pos @ last n chars
		lines = f.readlines()       # Read to end
	#print(lines)
	m = n - 1
	#print(lines [-n])
	#print('\n')
	#print(lines [-m])
	#print('\n')

	if lines [-n] == lines [-m]: #Makes sure duplicate lines are ignored
		lines = lines [-m]
		#print('same')
	else:
		lines = lines[-n:]    # Get last 10 lines
		#print('not')
	#print(lines)
	return lines


def action(lines,code):
	#print('Got it')    
	#print(time.strftime('%Y-%m-%d %I:%M:%S %p'), ' \n', lines)
	#print(code)
	log_an(lines,code)
	#names, emails = get_contacts('mycontacts.txt') # contactos
	#message_template = read_template('message.txt')
	#write_template(lines,code)
	#send_mail(names,emails,message_template,lines,code)
	#print("Notificación enviada al administrador")    

def log_an(lines,code):

	#print(code)
	if code == '%LINEPROTO-5-UPDOWN':
		start = lines.find(' r')
		hostname = lines[start+1:start+4]
		hostname = hostname.upper()
		#print(hostname)
		start = lines.find(' on ')
		end = lines.find(', changed')
		interface = lines[start+4:end]
		#print(interface)
		start = lines.find('to ')
		status = lines[start+3:-1]
		#print(status)
		end = lines.find(' r')
		date = lines[:end]
		#print(date)
		#print(len(status))
		if status == 'down':
			estado = 'inactivo'
		elif status == 'up':
			estado = 'activo'
		else:
			status == 'administrativamente inactivo' 
		notify = 'Se ha cambiado el estado de la interfaz '+ interface +' del router '+hostname+ ' a ' + estado + ' en '+ date+'.'
		print(notify)
	elif code == '%SYS-1-CPURISINGTHRESHOLD':
		start = lines.find(' r')
		hostname = lines[start+1:start+4]
		hostname = hostname.upper()
		start = lines.find('r)')
		end = lines.find('%/')
		cpu_usage = lines[start+4:end]
		#print(cpu_usage)
		#print(hostname)
		notify = 'Uso del CPU elevándose a un '+cpu_usage+' en '+hostname+'.'
	elif code == '%SYS-1-CPUFALLINGTHRESHOLD':
		start = lines.find(' r')
		hostname = lines[start+1:start+4]
		hostname = hostname.upper()
		start = lines.find('r)')
		end = lines.find('%/')
		cpu_usage = lines[start+4:end]
		notify = 'Uso del CPU descendiendo a un '+cpu_usage+' en '+hostname+'.'
	elif code == '%SYS-5-CONFIG_I: Configured from console by console':
		start = lines.find(' r')
		hostname = lines[start+1:start+4]
		hostname = hostname.upper()
		notify = 'Se ha entrado al modo configuración en el router '+hostname+'.'
	elif code == '%SYS-6-LOGGINGHOST_STARTSTOP: Logging to host 192.168.1.118 port 514 stopped':
		start = lines.find(' r')
		hostname = lines[start+1:start+4]
		hostname = hostname.upper()
		notify = 'El router '+hostname+' ha dejado de usar el servidor de logging.'
#Jun  2 19:00:05 r16 63: *Jun  2 19:00:07.463: %SYS-1-CPURISINGTHRESHOLD: Threshold: Total CPU Utilization(Total/Intr): 75%/100%, Top 3 processes(Pid/Util):  91/75%, 2/0%, 51/0%		
# %LINEPROTO-5-UPDOWN: Line protocol on Interface FastEthernet3/0, changed state to down

def log_monitor(log):
	
	LOG_FILE = '/var/log/snmp-logs/'+log+''

	print(
		'Watching of ' + LOG_FILE + ' at ' + time.strftime('%Y-%m-%d %I:%M:%S %p'))

	mtime_last = 0

	while True:
		mtime_cur = os.path.getmtime(LOG_FILE)    
		if mtime_cur != mtime_last:
			for i in tail(LOG_FILE, 2):
				for x in WATCH_FOR:
					if x.lower() in i.lower():	
						#print(i)						
						action(i,x)

		mtime_last = mtime_cur

		time.sleep(5)

def file_lengthy(fname):
	with open(fname) as f:
		for i, l in enumerate(f):
			pass
	return i + 1

def main():	
	threads = []
	lista = []
	listd = os.listdir("/var/log/snmp-logs/")
	#print(listd)
	for x in listd:
		if x[:1] == 'r':
			lista.append(x)
		else:
			pass
	#print(lista)

	fname = '../Pregunta1/outputs/host_live.list'
	
	for i in lista:
		t = threading.Thread(target=log_monitor, args = (i,))
		threads.append(t)
		t.start()

if __name__ == '__main__':
	main()