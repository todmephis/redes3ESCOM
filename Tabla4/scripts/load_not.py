import MySQLdb
import os
import sys
import subprocess
import collections
import time
import datetime
import mmap
import smtplib
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import telegram
import sys

#DB_IP='10.100.64.50'
#DB_IP='192.168.200.13'

def Not_load(titulo,mensaje,router):#Loads data into several tables
	#print('sss')
	#os.system('sudo service mysql start')
	#os.system('sudo service mysql.server start')
	#Building a query 
	now = datetime.datetime.now()
	date = now.strftime("%Y-%m-%d %H:%M")
	#database = MySQLdb.connect (host="localhost", user = "root", passwd = "root")																	  																				  
	database = MySQLdb.connect (host='192.168.200.13', user = "netuser", passwd = "123") 
	cursor = database.cursor()	
	cursor._defer_warnings = True
	query = 'select idDispositivo from redes3proj.Dispositivo WHERE nombre = "'+router+'"'
	cursor.execute(query)
	ret = cursor.fetchall()
	print('jsjs',ret)
	id = int(ret[0][0])
	query = "INSERT INTO redes3proj.Notificacion (titulo,mensaje,Dispositivo_idDispositivo)" \
			"VALUES ( %s, %s, %s)"
	args = (titulo, mensaje,id)
	cursor.execute(query,args)
	print(cursor._last_executed)
	database.commit()
	database.close()

