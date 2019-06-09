
import smtplib
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import telegram

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

def write_template(message,lines,template):
	#Se escribe el archivo que se enviará con el reporte de las subredes:
	outF = open(template, "w")
	outF.write(message)
	repF = open(lines, "r")
	for x in repF:
		outF.write(x)
	repF.close()
	#outF.write(''+lines+'\n')
	outF.close()

def send_mail(names,emails,message_template,subject,template,notificacion_t):
	'''
	repF = open(template,"r")
	notificacion_t =''
	noti = ''
	for x in repF:
		notificacion_t = noti+repF.readline()
		noti = notificacion_t
	'''
	try:
		bot = telegram.Bot(token='551346453:AAHdw97BnU_cv-i4FUmvtYKDEvkHTkbMSno') #TelegramBot Token
		print("[DEBUG] {}".format(bot.get_me()))
		bot.send_message(chat_id='8288143', text=notificacion_t) #Set chat_id
	except:
		print('Notificación de Telegram fallida, no hay conexión a internet.')
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
	except:
		print('Notificación de correo electrónico fallida, no hay conexión a internet.')