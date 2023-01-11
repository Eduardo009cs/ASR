import telnetlib
from ftplib import FTP
import subprocess

HOST = "30.30.30.1"
user = "rcp"
pas = "rcp"

#tn = telnetlib.Telnet()
#tn.open(HOST)
#tn.read_until(b"User: ")
#tn.write(user.encode("ascii")+b"\r\n")
#tn.read_until(b"Password: ")
#tn.write(pas.encode("ascii")+b"\r\n")
#tn.write(b"en\r\n")
#tn.write(b"show interface\r\n")
#tn.write(b"exit\r\n")

#print(tn.read_all())
#tn.close()


"""def agregarTelnet(ip,adap,host):
	tn = telnetlib.Telnet()
	tn.open(host)
	tn.read_until(b"User: ")
	tn.write(user.encode("ascii")+b"\r\n")
	tn.read_until(b"Password: ")
	tn.write(pas.encode("ascii")+b"\r\n")
	tn.write(b"en\r\n")
	tn.write(b"config\r\n")
	cad = "interface ethernet eth" + adap
	cad2 = "ip address " + ip + "/24"
	#print(cad)
	#print(cad2)
	tn.write(cad.encode("ascii") + b"\r\n")
	tn.write(cad2.encode("ascii") + b"\r\n")
	tn.write(b"no sh\r\n")
	tn.write(b"exit\r\n")
	tn.write(b"show interface\r\n")
	network = "network " + ip[0:len(ip)-1] + "0/24"
	#print(network)
	tn.write(b"router rip\r\n")
	tn.write(network.encode("ascii") + b"\r\n")
	tn.write(b"exit\r\n")
	tn.write(b"exit\r\n")
	tn.write(b"exit\r\n")
	tn.write(b"exit\r\n")
	tn.read_all()
	tn.close()

def agregarNodo():
	print("\n--------------------------AGREGAR NODO--------------------------")
	
	nombre = input("Ingrese el nombre del nodo: ")
	outfile = open('nodos_guardados.txt','a')
	outfile.write(nombre)
	outfile.write("\n")
	outfile.close()
	
		
		
	menu()



def agregarConexion():
	print("\n--------------------------AGREGAR CONEXION--------------------------")
	print("\nIndique el router al que se quiere conectar")
	f = open('nodos_guardados.txt','r')
	routers = f.readlines()
	f.close
	i = 0
	while i< len(routers):
		print(i + 1, ".-",routers[i])
		i+=1
	aux = input()
	opc = int(aux) - 1
	router = routers[opc]
	print("\nIndique la ip: ")
	ip = input()
	print("\nIndique el adaptador (0-3): " )
	adap = input()
	print("\nProporcione la ip para realizar la conexion con el router:")
	host = input()
	
	agregarTelnet(ip,adap,host)
	menu()
			
def crearArchivoConfiguracion():
	print("\n--------------------------CREAR ARCHIVO DE CONFIGURACION--------------------------")
	print("\nIndique el router al que se quiere conectar")
	f = open('nodos_guardados.txt','r')
	routers = f.readlines()
	f.close
	i = 0
	while i< len(routers):
		print(i + 1, ".-",routers[i])
		i+=1
	aux = input()
	opc = int(aux) - 1
	router = routers[opc]
	print("\nProporcione la ip para realizar la conexion con el router:")
	host = input()
	tn = telnetlib.Telnet()
	tn.open(host)
	tn.read_until(b"User: ")
	tn.write(user.encode("ascii")+b"\r\n")
	tn.read_until(b"Password: ")
	tn.write(pas.encode("ascii")+b"\r\n")
	tn.write(b"en\r\n")
	tn.write(b"config\r\n")
	tn.write(b"copy run start\r\n")
	tn.write(b"exit\r\n")
	tn.write(b"exit\r\n")
	tn.write(b"exit\r\n")
	tn.read_all()
	tn.close()
	print("*****ARCHIVO DE CONFIGURACION CREADO*****")
	menu()
	
def recuperarArchivo():
	print("\n--------------------------RECUPERAR ARCHIVO DE CONFIGURACION--------------------------")
	print("\nIndique el router al que se quiere conectar")
	f = open('nodos_guardados.txt','r')
	routers = f.readlines()
	f.close
	i = 0
	while i< len(routers):
		print(i + 1, ".-",routers[i])
		i+=1
	aux = input()
	opc = int(aux) - 1
	router = routers[opc]
	print("\nProporcione la ip para realizar la conexion con el router:")
	host = input()
	tn = telnetlib.Telnet()
	tn.open(host)
	tn.read_until(b"User: ")
	tn.write(user.encode("ascii")+b"\r\n")
	tn.read_until(b"Password: ")
	tn.write(pas.encode("ascii")+b"\r\n")
	tn.write(b"en\r\n")
	tn.write(b"config\r\n")
	tn.write(b"service ftp\r\n")
	tn.write(b"exit\r\n")
	tn.write(b"exit\r\n")
	tn.write(b"exit\r\n")
	tn.read_all()
	tn.close()
	
	ftp = FTP (host)
	ftp.login(user,pas)
	ftp.retrbinary('RETR startup-config',open('startup-config-' + router + ".txt", 'wb').write)
	ftp.quit()
	print("*****ARCHIVO DE CONFIGURACION DESCARGADO*****")
	menu()
def agregarNodoFinal():
	print("\n--------------------------AGREGAR NODO FINAL--------------------------")
	
	nombre = input("Ingrese la ip del nodo final: ")
	outfile = open('nodos_final_guardados.txt','a')
	outfile.write(nombre)
	outfile.write("\n")
	outfile.close()	
	menu()
def verificarConexion():
	
	print("\n--------------------------VERIFICAR CONEXION NODO FINAL--------------------------")
	print("\nSeleccione la ip que quiere verificar")
	f = open('nodos_final_guardados.txt','r')
	ips = f.readlines()
	f.close
	i = 0
	while i< len(ips):
		print(i + 1, ".-",ips[i])
		i+=1
	aux = input()
	opc = int(aux) - 1
	ip = ips[opc]
	p = subprocess.Popen('ping ' + ip, stdout = subprocess.PIPE)
	p.wait()
	if p.poll():
		print (ip + " is down")
	else:
		print (ip + "  is up")
	menu()"""
def generarArchivo():
	print("\nProporcione la ip para realizar la conexion con el router:")
	host = input()
	tn = telnetlib.Telnet()
	tn.open(host)
	tn.read_until(b"User: ")
	tn.write(user.encode("ascii")+b"\r\n")
	tn.read_until(b"Password: ")
	tn.write(pas.encode("ascii")+b"\r\n")
	tn.write(b"en\r\n")
	tn.write(b"config\r\n")
	tn.write(b"copy run start\r\n")
	tn.write(b"exit\r\n")
	tn.write(b"exit\r\n")
	tn.write(b"exit\r\n")
	tn.read_all()
	tn.close()
	print("*****ARCHIVO DE CONFIGURACION CREADO*****")
	menu()
def extraerArchivo():
	print("\nProporcione la ip para realizar la conexion con el router:")
	host = input()
	
	
	ftp = FTP (host)
	ftp.login(user,pas)
	ftp.retrbinary('RETR startup-config',open('startup-config' , 'wb').write)
	ftp.quit()
	print("*****ARCHIVO DE CONFIGURACION DESCARGADO*****")
	menu()
def importarArchivo():
	print("\nProporcione la ip para realizar la conexion con el router:")
	host = input()
	
	
	ftp = FTP (host)
	ftp.login(user,pas)
	f = open('startup-config','rb')
	ftp.storbinary('STOR startup-config',f)
	f.close()
	ftp.quit()
	print("*****ARCHIVO DE CONFIGURACIO ENVIADO*****")
	menu()
	
def menu():
	print("--------------------------SISTEMA DE ADMINISTRACION--------------------------")
	print("1. Generar el archivo de configuración")
	print("2. Extraer el archivo de configuración.")
	print("3. Importar el archivo de configuración.")
	opc = input()
	if opc =="1":
		generarArchivo()
	if opc == "2":
		extraerArchivo()
	if opc == "3":
		importarArchivo()
	
	if opc > "3" or opc < "1":
		exit()
	

menu()
