#!/usr/bin/env python

import os
import sys
import subprocess
import collections
import time
import mmap
import smtplib
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import telegram
from itertools import tee
import sendmail


CONTACTS = '../inputs/mycontacts.txt'
MAIL_TEMPL = '..reports/template.txt'
try:

    LOG_FILE = os.path.abspath('/var/log/syslog')
    WATCH_FOR =  '.9.9.43.1' #config
    #WATCH_FOR2 = '.9.9.109' #cpu
    #WATCH_FOR3 = '.9.9.13.3.0.7' #temp change
    #WATCH_FOR4 = '.9.2.1.2.0' #shutdown
except:

    sys.stderr.write(
        'Usage: %s [log file] [string to watch for]' % sys.argv[0])
    sys.exit(1)

def action(lines):
    l = []
#   if 'beep' in sys.argv:

#      subprocess.Popen(['paplay', '/usr/share/sounds/ubuntu/notifications/Mallet.ogg'])

    #if 'notify' in sys.argv:

    #   subprocess.Popen(['notify-send', 'LogMonitor', 'Found!'])
    #hostname = lines.split('R')[1]
    print(lines)
    i=0
    while i < 1:
        pos = lines.find('R')
        if lines[pos+1].isdigit() and lines[pos+2].isdigit():
            hostname = lines[pos]+lines[pos+1]+lines[pos+2]
            print(hostname.lower())
            log = '/var/log/snmp-logs/'+hostname.lower()+'.log'
            os.system('tail '+log+' > /tftpboot/snmp_manager/reports/'+hostname+'')
            mail('/tftpboot/snmp_manager/reports/'+hostname+'',hostname)
            i+=1
        else:
            pass

    """
    exists = os.path.isfile('/tftpboot/snmp_manager/outputs/trap_own')
    if exists:
        os.system('echo "'+hostname+'" > /tftpboot/snmp_manager/outputs/trap_own')
    else:
        os.system('touch /tftpboot/snmp_manager/outputs/trap_own')
        os.system('echo "'+hostname+'" > /tftpboot/snmp_manager/outputs/trap_own')
    os.system('/tftpboot/snmp_manager/scripts/auditor.sh A trap_own')
    changes_file = '/tftpboot/snmp_manager/outputs/changes/changes_'+hostname+''
    print(changes_file)
    exists = os.path.isfile(changes_file)
    if exists:
        print('Done')
        f = open(changes_file,"r")
        f1 = f.readlines()
        for x in f1:
            l.append(x)
            if '|' in x:


        os.system('cat '+changes_file+'')
    """

def mail(report,host):
    names, emails = sendmail.get_contacts(CONTACTS)
    message_template = sendmail.read_template(MAIL_TEMPL)
    message = 'Ha cambiado la configuración del router'+host+':'+'\n'+''
    sendmail.write_template(message,report,MAIL_TEMPL)
    sendmail.send_mail(names,emails,message_template,'Notificación SNMP',MAIL_TEMPL)



def tail(file, n):

    with open(file, "r") as f:

        f.seek (0, 2)         # Seek @ EOF
        fsize = f.tell()        # Get Size
        f.seek (max (fsize-1024, 0), 0) # Set pos @ last n chars
        lines = f.readlines()      # Read to end

    lines = lines[-n:]  # Get last 10 lines

    return lines

#os.system("sudo snmptrapd -L s 127.0.0.1")
os.system("sudo snmptrapd -L s 192.168.1.117")

print(
    'Watching of ' + LOG_FILE + ' for SNMP Traps started at ' + time.strftime('%Y-%m-%d %I:%M:%S %p'))

mtime_last = 0

while True:
	mtime_cur = os.path.getmtime(LOG_FILE)
	if mtime_cur != mtime_last:
		for i in tail(LOG_FILE, 5):
			if WATCH_FOR.lower() in i.lower():
				action(i) #shutdown
				break
	mtime_last = mtime_cur
	time.sleep(5)
