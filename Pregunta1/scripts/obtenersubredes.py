import getpass
import keyboard
import telnetlib
import json
import sys
#Nombre recomendado: subnets.list
#Accedemos mediante telnet a un router dentro de la red y obtenemos su tabla de ruteo
#la cual tiene todas las subredes de la red

HOST = "10.0.2.2"
user = raw_input("Enter your remote account: ")
password = getpass.getpass()

tn = telnetlib.Telnet(HOST)

tn.read_until("Username: ")
tn.write(user + "\n")
if password:
    tn.read_until("Password: ")
    tn.write(password + "\n")

tn.write("en\n")
tn.write("cisco\n")
tn.write("terminal length 0\n")
tn.write("show ip route\n")
tn.write("exit\n")
a=tn.read_all()

#Guardamos eso en un archivo
try:
    f = open (sys.argv[1],'w')
except Exception as e:
    print(e)
    exit(-1 )
f.write(a)
f.close()
h=0 
#Empezamos limpiando todo lo que no nos interesa

lineas=[]
with open(sys.argv[1], 'r') as f:
	for linea in f:
		if(linea.find("Gateway")==0):
			h=1
		if(h==1):
			lineas.append(linea.split())

#Obtenemos solo los identificadores de red del archivo

i=4
redes=[]
redes3=""
while i<len(lineas)-1:
	if(lineas[i][0]=="O" and lineas[i][2][len(lineas[i][2])-2:len(lineas[i][2])]!="32"):
		redes3=redes3+lineas[i][2]+"\n"
	if(lineas[i][0]=="C"):		
		redes3=redes3+lineas[i][1]+"\n"
	i=i+1

#Lo guardamos en el mismo archivo
try:
    f = open (sys.argv[1],'w')
except Exception as e:
    print(e)
    exit(-1 )
f.write(redes3)
f.close()