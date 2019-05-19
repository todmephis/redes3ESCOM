import MySQLdb
import os
import sys
import datetime

def create_database():
	#database connection
	database = MySQLdb.connect (host="localhost", user = "root", passwd = "root") #connection user and password have been hardcoded given
																				  #the nature of the excercise. I'm aware credentials should be 
																				  #encrypted or secured for security reasons.
	cursor = database.cursor()													  
	cursor._defer_warnings = True
	for line in open('/tftpboot/snmp_manager/scripts/db'):
		#print('DEBUG:',line) #debug
		cursor.execute(line)
	print('DEBUG: Database is up')

def process_inv_file(router):
	d = {}
	dict_list = []
	data = ['NAME','DESCR','PID','VID','SN']
	try:
		with open ('/tftpboot/snmp_manager/inventory/'+router+'', 'rt') as file:  
			for line in file:                 
				#print(line)                     
				for x in data:
					pos = line.find(x)
					if pos != -1 : #Attribute found
						startIndex = (line[pos:].find('\"')+1+pos)
						if startIndex > 0: #i.e. if the first quote was found
							endIndex = line.find('\"', startIndex + 1)
							if startIndex != -1 and endIndex != -1: #i.e. both quotes were found
								param = line[startIndex:endIndex]
								#print(x,':',param)
								d[x]= param
							else:
								index = (line[startIndex:].find(' ')+1+startIndex)
								endIndex = (line[index:].find(' ')+1+startIndex)
								param = line[index:endIndex]
								if isinstance(param,str) or isinstance(param,int):
									pass
								else:
									param = 'N/A'
								#print(x,':',param)
								d[x]= param
						elif startIndex == 0:
							#print(startIndex)
							startIndex = (line[pos:].find(' ')+1+pos)
							if startIndex != -1: 
								endIndex = line.find(' ',startIndex + 1)
								#print(endIndex)
								if startIndex != -1 and endIndex != -1: 
									param = line[startIndex:endIndex]
									#print(x,':',param)
									d[x]= param
									#print(param)
							else: 
								param = 'N/A'
								d[x]= param
						if x == 'SN':
							#dict_list.append(d)
							print(d)
							Load(d,router)
					else:
						pass
			else:
				if line < 3:
					print('ERROR: Inventory file for router ' +router+ ' not fetched correctly !')		
		file.close()
		os.system('mysql --host localhost --user root --password=root -D snmp -e "select * from snmp.inventario;"')
	except:
		print('ERROR: Inventory file for router ' +router+ ' not found !')
		return 0

def Load(args,router):#Loads data into several tables
	#Building a query 
	now = datetime.datetime.now()
	date = now.strftime("%Y-%m-%d %H:%M")
	database = MySQLdb.connect (host="localhost", user = "root", passwd = "root")																	  																				  
	cursor = database.cursor()	
	query = "INSERT INTO snmp.inventario (Router,Nombre,Descripcion,PID,VID,NS,Date_Time)" \
			"VALUES ( %s, %s, %s, %s, %s, %s, %s)"
	args = (router,args['NAME'],args['DESCR'],args['PID'],args['VID'],args['SN'],date)
	cursor.execute(query,args)
	database.commit()
	database.close()


def main():
	create_database()
	process_inv_file(sys.argv[1])

if __name__ == '__main__':
	main()