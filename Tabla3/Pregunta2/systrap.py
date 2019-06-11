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
import sys
from load_not import Not_load

f = open('data','r')	

MY_ADDRESS = 'redes3@todmephis.cf'
PASSWORD = 'ZxBuOWYR8S#f'
SMTP_HOST = 'mail.todmephis.cf' 
SMTP_PORT = '26'
BOT_TOKEN = '551346453:AAHdw97BnU_cv-i4FUmvtYKDEvkHTkbMSno'
TELEGRAM_ID = '8288143'

LOG_FILE = os.path.abspath('/var/log/syslog')
WATCH_FOR =  '.9.9.43.1' #config
WATCH_FOR2 = '.9.9.109' #cpu
WATCH_FOR3 = '.9.9.13.3.0.7' #temp change
WATCH_FOR4 = '.9.2.1.2.0' #shutdown

def action(lines,code):
	start = lines.find(' R')
	hostname = lines[start+1:start+4]
	hostname = hostname.upper()
	if 'notify' in sys.argv:

		subprocess.Popen(['notify-send', 'LogMonitor', 'Found!'])
	print('Got it')    
	print(time.strftime('%Y-%m-%d %I:%M:%S %p'), ' \n', i)
	names, emails = get_contacts('mycontacts.txt') # contactos
	message_template = read_template('message.txt')
	write_template(lines,code)
	#print('aa')
	send_mail(names,emails,message_template,lines,code,'Notificacion SNMP',hostname)
	#print("Notificación enviada al administrador")    

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

def send_mail(names,emails,message_template,lines,code,subject,hostname):
	#try:
	bot = telegram.Bot(token='551346453:AAHdw97BnU_cv-i4FUmvtYKDEvkHTkbMSno')
	#print("[DEBUG] {}".format(bot.get_me()))
	if code == 0: 
		spec = 'Han habido cambios configuración. \n'
		notificacion_t = 'Notificación SNMP: Ha llegado una trap al Servidor: '+ str(lines)+ '.\n'+spec
	elif code == 1:
		spec = 'El CPU ha rebasado el porcentaje de uso.\n'
		notificacion_t = 'Notificación SNMP: Ha llegado una trap al Servidor: '+ str(lines)+ '.\n'+spec
	elif code == 2:
		spec = 'Cambio de temperatura detectada con el sensor I/O Cont Inlet.\n'
		notificacion_t = 'Notificación SNMP: Ha llegado una trap al Servidor: '+ str(lines)+ '.\n'+spec
	elif code == 3:
		spec = 'Se ha apagado un router\n' 
		notificacion_t = 'Notificación SNMP: Ha llegado una trap al Servidor: '+ str(lines)+ '.\n'+spec
	else: 
		print("Unknown code")
	try:
		Not_load('Trap-SNMP',spec,hostname)
	except:
		print('')
	bot.send_message(chat_id='8288143', text=notificacion_t) #Set chat_id
	print('Notificación enviada por Telegram')
	#except Exception as e:
	#	print(e)
	#	print('Notificación de Telegram fallida, no hay conexión a internet.')
	'''
	try:	
		# SMTP Server:
		s = smtplib.SMTP(host='mail.todmephis.cf', port=26)#Configuración de email
		s.starttls()
		s.login('redes3@todmephis.cf', 'ZxBuOWYR8S#f')

		for name, email in zip(names, emails):
			msg = MIMEMultipart()       # msg mime
			message = message_template.substitute(DEPARTMENT_NAME=name.title())

			#Vista previa:
			print(message)

			# Parametros del mensaje:
			msg['From']='redes3@todmephis.cf'
			msg['To']=email
			msg['Subject']=subject

			# Cuerpo del mensaje
			msg.attach(MIMEText(message, 'plain'))
			#(mensaje,texto)

			# Enviar.
			s.send_message(msg)
			del msg

		# Cierra la conexión con el servidor SMTP
		s.quit()
		print('Notificación de correo electrónico enviada.')
	except Exception as e: 
		print(e)
		print('Notificación de correo electrónco fallida, no hay conexión a internet.')
	'''
#os.system("sudo snmptrapd -L s 127.0.0.1")
print(
	'Buscando en ' + LOG_FILE + '  SNMP Traps  ' + time.strftime('%Y-%m-%d %I:%M:%S %p'))

mtime_last = 0
#f = open('')
#for line in f
os.system("sudo snmptrapd -L s 192.168.1.117")

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
