import getpass
import keyboard
import telnetlib
import json
import sys
import os

lista=[]
#Este archivo es donde tienes guardado los host que contestaron el script de la pregunta 1 de la tabla 3
import os
if not os.path.exists('/tftpboot/conf_files/'):
    os.makedirs('/tftpboot/conf_files')


with open ('../Pregunta1/outputs/host_live.list','r') as f:
	va =[linea.split() for linea in f]
#print str(va)
i=0
#Descomenta el while de abajo y agrega la ruta que quieras para guardar los archivos de configuración, y en este caso se llaman r1...rn
while i<len(va)-1:
	os.system("tftp "+ str(va[i][0]) +" << TFTP\n get startup-config /tftpboot/conf_files/r"+str(i)+"\nquit\n TFTP")
	i=i+1

i=1
while i<len(va)-1:
	with open ('/tftpboot/conf_files/r'+str(i),'r') as f: #Aqui cambia la ruta a donde tengas guardados los archivos de configuración de los routers, aqui tomo como base que se llaman r'número de archivo de configuración'
		router =[linea.split() for linea in f]
	i=i+1
	lista.append(router[12][1])
#print lista


lista_nueva = []
lista_ips=""
j=0
for k in lista:
     if k not in lista_nueva:
         lista_nueva.append(k)
         lista_ips+= (str(va[j][0]))+"\n"
     j=j+1

print (lista_nueva) #Aqui está el nombre de los routers
print (lista_ips)	#Aqui esta la ip de los de arriba
f = open ('/../Pregunta1/outputs/ip_routers.txt','w') #En este archivo solo se guarda la ip de los host
f.write(lista_ips)
f.close()

f = open ('/../Pregunta1/outputs/hostnames.txt','w') #En este archivo solo se guarda los nombres de los host
f.write(lista_nueva)
f.close()
