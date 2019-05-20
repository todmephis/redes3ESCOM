import os
def generate_t(file,args,ofile):
	variables = ['%h','%u','%lh','%sh','%pass']
	args.reverse()
	print(args)

	with open(file, "rt") as fin:
		with open(ofile, "wt") as fout:
			for line in fin:
				for x in variables:
					#print(variables)
					pos = line.find(x)
					if pos != -1:
						if x == '%u':
							#print(variables)
							fout.write(line.replace(x,args.pop()).replace('%lp',args.pop()))
							print(x)
							break
						else:
							fout.write(line.replace(x,args.pop()))
							break
				if pos == -1:
					fout.write(line)
	fin.close()
	fout.close()
	"""
	with open (file,"rt") as lines:
		for line in lines:
			for x in variables:
				pos=line.find(x)
				if pos!= -1:
					line = line[:pos]+args.pop()
	"""


def main():
	infile='../templates/template'
	args = []
	print('Ingrese parámetros del archivo de configuración')
	args.append(input('Hostname: '))
	args.append(input('Usuario: '))
	args.append(input('Contraseña: '))
	args.append(input('Host de logging: '))
	args.append(input('Servidor snmp: '))
	args.append(input('Enable password: '))
	ofile='../templates/template'+args[0]+''
	print(ofile)
	#print(args)
	#Hostname,username,login pass,logging host,snmp server address, password

	#os.system('sudo cp ../templates/template ../templates/template'+args[0]+'')
	print('Generando template...')
	generate_t(infile,args,ofile)

if __name__ == '__main__':
	main()
