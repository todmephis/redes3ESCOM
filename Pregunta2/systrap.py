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

f = open('data','r')	

MY_ADDRESS = f.readline()
PASSWORD = f.readline()
SMTP_HOST = f.readline()
SMTP_PORT = f.readline()
BOT_TOKEN = f.readline()
TELEGRAM_ID = f.readline()

try:

    LOG_FILE = os.path.abspath('/var/log/syslog')
    WATCH_FOR =  '.9.9.43.1' #config
    WATCH_FOR2 = '.9.9.109' #cpu
    WATCH_FOR3 = '.9.9.13.3.0.7' #temp change
    WATCH_FOR4 = '.9.2.1.2.0' #shutdown
except:

    sys.stderr.write(
        'Usage: %s [log file] [string to watch for]' % sys.argv[0])
    sys.exit(1)

def action(lines,code):

    if 'beep' in sys.argv:

        subprocess.Popen(['paplay', '/usr/share/sounds/ubuntu/notifications/Mallet.ogg'])

    if 'notify' in sys.argv:

        subprocess.Popen(['notify-send', 'LogMonitor', 'Found!'])
    print('Got it')    
    print(time.strftime('%Y-%m-%d %I:%M:%S %p'), ' \n', i)
    names, emails = get_contacts('mycontacts.txt') # contactos
    message_template = read_template('message.txt')
    write_template(lines,code)
    send_mail(names,emails,message_template,lines,code)
    print("Notificación enviada al administrador")    

# basic Python implementation of Unix tail

def tail(file, n):

    with open(file, "r") as f:

        f.seek (0, 2)           # Seek @ EOF
        fsize = f.tell()        # Get Size
        f.seek (max (fsize-1024, 0), 0) # Set pos @ last n chars
        lines = f.readlines()       # Read to end

    lines = lines[-n:]    # Get last 10 lines

    return lines

def get_contacts(filename):
    """
    Regresa listas con nombres y emails
    """
    
    names = []
    emails = []
    with open(filename, mode='r', encoding='utf-8') as contacts_file:
        for a_contact in contacts_file:
            names.append(a_contact.split()[0])
            emails.append(a_contact.split()[1])
    return names, emails

def read_template(filename):
    """
    Objeto plantilla.
    """
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)

def write_template(lines,code):
    #Se escribe el archivo que se enviará con el reporte de las subredes:

    #test_list=["One","Two","Three","Four","How many nibbas are in my store?"]
    outF = open("message.txt", "w")
    outF.write('($DEPARTMENT_NAME)')
    outF.write('.\n')
    outF.write('El sistema SNMP ha levantado una notificación.\n')
    outF.write('Ha llegado una trap al servidor:\n')
    outF.write(''+ str(lines)+'\n')
    if code == 0:
    	outF.write('Se han hecho cambios a la configuración del agente.\n')
    if code == 1:
    	outF.write('Ha habido un pico en el uso del CPU, se ha rebasado el límite establecido (80%).\n')
    	outF.write('El agente requiere de atención urgente.\n')
    if code == 2:
    	outF.write('Cambio de temperatura detectada con el sensor I/O Cont Inlet.')
    if code == 3:
    	outF.write('Se ha apagado un router.')
    #if ''
    outF.close()

def send_mail(names,emails,message_template,lines,code):
	bot = telegram.Bot(token=BOT_TOKEN) #TelegramBot Token
	print("[DEBUG] {}".format(bot.get_me()))
	if code == 0: 
		notificacion_t = 'Notificación SNMP: Ha llegado una trap al Servidor: '+ str(lines)+ '.\n'+'Ha habido cambios en la configuración. \n'
	elif code == 1:
		notificacion_t = 'Notificación SNMP: Ha llegado una trap al Servidor: '+ str(lines)+ '.\n'+ 'El CPU ha rebasado el porcentaje de alerta de uso.\n'
	elif code == 2:
		notificacion_t = 'Notificación SNMP: Ha llegado una trap al Servidor: '+ str(lines)+ '.\n'+ 'Cambio de temperatura detectada con el sensor I/O Cont Inlet.\n'
	elif code == 3:
		notificacion_t = 'Notificación SNMP: Ha llegado una trap al Servidor: '+ str(lines)+ '.\n'+ 'Se ha apagado un router\n'
	else: 
		print("Unknown code")

	bot.send_message(chat_id=TELEGRAM_ID, text=notificacion_t) #Set chat_id
    
    # SMTP Server:
	s = smtplib.SMTP(host=SMTP_HOST, port=SMTP_PORT) #Configuración de email
	s.starttls()
	s.login(MY_ADDRESS, PASSWORD)

	for name, email in zip(names, emails):
		msg = MIMEMultipart()       # msg mime

		message = message_template.substitute(DEPARTMENT_NAME=name.title())     

        #Vista previa:
		print(message)

        # Parametros del mensaje:
		msg['From']=MY_ADDRESS
		msg['To']=email
		msg['Subject']="Notificación SNMP"
        
        # Cuerpo del mensaje
		msg.attach(MIMEText(message, 'plain'))
        #(mensaje,texto)
        
        # Enviar.
		s.send_message(msg)
		del msg
        
    # Cierra la conexión con el servidor SMTP
	s.quit()


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
				action(i,0) #CONF
			elif WATCH_FOR2.lower() in i.lower():
				action(i,1) #cpu
			elif WATCH_FOR3.lower() in i.lower():
				action(i,2) #temp change
			elif WATCH_FOR4.lower () in i.lower():
				action(i,3) #shutdown

	mtime_last = mtime_cur

	time.sleep(5)
