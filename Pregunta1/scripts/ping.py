import smtplib
import sys
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import telegram

MY_ADDRESS = 'correo@dominio.com' #Dirección de Email
PASSWORD = '*****' #Password


def get_ips():    
#Obtenemos las ip que checaremos
    with open(sys.argv[1], 'r',encoding = 'utf-8') as f:
        lista3 = [linea.split() for linea in f]
    print(lista3)
    return lista3

def polling(lista3):
bot = telegram.Bot(token='') #TelegramBot Token
print("[DEBUG] {}".format(bot.get_me()))
    i=0
    lista1= []
    lista2= []
    contPing = 0
    contResp1 = 0
    contResp2 = 0
    contResp3 = 0
    percen1 = 0
    percen2 = 0
    percen3 = 0
    #notify=0
    cadena = ""

    while i<len(lista3):
        response = os.system("ping -c 1 " + lista3[i][0])
        if response ==0:
            lista1.append(lista3[i])
        else:
            response = os.system(" ping -c 1 " + lista3[i][0])
            if response ==0:
                lista1.append(lista3[i])
                contResp1 = contResp1 + 1 
                print("Alerta 1 nivel bajo \n",end="")
                percen1 = contResp1 * 10
                print ("Porcentaje de paquetes exitosos: ", percen1, "%")
                notificacion_t = "Alerta 1 nivel bajo\nPorcentaje de paquetes exitosos:" + str(percen1) + "%"
                bot.send_message(chat_id="", text=notificacion_t) #Set chat_id

                #notify = 1

            else:
                response = os.system("ping -c 1 " + lista3[i][0])
                if response ==0:
                    lista1.append(lista3[i]) 
                    contResp2 = contResp1 + 1 
                    print("Alerta 2 nivel medio  \n",end="")
                    percen2 = contResp1 * 10
                    print("Porcentaje de paquetes exitosos: " , percen2 , "%")
                    notificacion_t = "Alerta 2 nivel medio\nPorcentaje de paquetes exitosos:" + str(percen2) + "%"
                    bot.send_message(chat_id="", text=notificacion_t)  #Set chat_id   
                    #notify=1    
                else:
                    lista2.append(lista3[i])
                    contResp3 = contResp3 + 1 
                    print("Alerta 3 nivel alto \n",end="")
                    percen3 = contResp3 * 10
                    print("Porcentaje de paquetes exitosos: " , percen3 , "%")
                    notificacion_t = "Alerta 3 nivel alto\nPorcentaje de paquetes exitosos:" + str(percen3) + "%"
                    bot.send_message(chat_id="", text=notificacion_t)#Set chat_id
                    #notify=1    
        i=i+1

    print("Redes disponibles:\n")
    print(lista1)
    print("Redes no disponibles:\n")
    print(lista2)
    return lista1,lista2

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

def write_template(lista1,lista2):
    #Se escribe el archivo que se enviará con el reporte de las subredes:

    #test_list=["One","Two","Three","Four","How many nibbas are in my store?"]
    outF = open("message.txt", "w")
    outF.write('($DEPARTMENT_NAME)')
    outF.write('Se han encontrado fallos mediante polling.\n')
    outF.write('El sistema SNMP ha levantado una notificación.\n')
    outF.write('Las siguientes subredes han fallado en responder:\n')
    #Subredes inactivas
    for line in lista2:
        print(line)
        outF.write(str(line))
        outF.write('\n')
    
    outF.write('\n')
    outF.write('\n')
    outF.write('Subredes que han respondido exitosamente al polling:\n')
    #Subredes activas:
    for line in lista1:
        outF.write(str(line))
        outF.write('\n')
    
    outF.close()

def send_mail(names,emails,message_template):
    # SMTP Server:
    s = smtplib.SMTP(host='mail.dominio.com', port=26) #Configuración de email
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


def main():
    lista3 = get_ips()
    lista1 , lista2  = polling(lista3)
    write_template(lista1,lista2)
    print("Marca")
    names, emails = get_contacts('mycontacts.txt') # contactos
    message_template = read_template('message.txt')
    send_mail(names,emails,message_template)
    print("Notificación enviada al administrador")    
    print("Hecho.")
    
if __name__ == '__main__':
    main()

