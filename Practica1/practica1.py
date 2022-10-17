#EduardoCuevasSolorza s
from email.policy import default
from reportlab.pdfgen import canvas
from reportlab.platypus import (SimpleDocTemplate, PageBreak, Image, Spacer,
Paragraph, Table, TableStyle)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from pysnmp.hlapi import *
from datetime import datetime


width, height = A4
def coord(x, y, unit=1):
    x, y = x * unit, height -  y * unit
    return x, y
def agregarDispositivo():
    print("\n------------------------------AGREGAR------------------------------")
    comunidad = input("Comunidad: ")
    version = input("Version SNMP: ")
    puerto = input("Puerto: ")
    ip = input("IP: ")

    dispositivo = comunidad + " " + version + " " + puerto + " " + ip
    outfile =  open('dispositivos_guardados.txt','a')
    outfile.write(dispositivo)
    outfile.write("\n")
    outfile.close()
    menu()


    
def editarDispositivo():
    print("\n------------------------------EDITAR------------------------------")
    f = open('dispositivos_guardados.txt','r')
    #dispositivos = f.read()
    dispositivos = f.readlines()
    f.close()
    print("Elija un dispositivo:\n")
    i=0
    while i<len(dispositivos):
        print(i + 1,".- ",dispositivos[i])
        i+=1
    aux = input()
    opc = int(aux) - 1
    comunidad = input("Nueva Comunidad: ")
    version = input("Nueva Version SNMP: ")
    puerto = input("Nuevo Puerto: ")
    ip = input("Nueva IP: ")
    dispositivos[opc] = comunidad + " " + version + " " + puerto + " " + ip
    i=0
    f = open('dispositivos_guardados.txt','w')
    while i < len(dispositivos) :
        f.write(dispositivos[i])
        if i != len(dispositivos) - 1:
            f.write("\n")
        i+=1
    f.close()
    menu()

def eliminarDispositivo():

    print("\n------------------------------ELIMINAR------------------------------")
    f = open('dispositivos_guardados.txt','r')
    #dispositivos = f.read()
    dispositivos = f.readlines()
    f.close()
    print("Elija un dispositivo:\n")
    i=0
    while i<len(dispositivos):
        print(i + 1,".- ",dispositivos[i])
        i+=1
    aux = input()
    opc = int(aux) - 1
    f = open('dispositivos_guardados.txt','w')
    i=0
    while i < len(dispositivos) :
        if i != opc:
            f.write(dispositivos[i])
            if i != len(dispositivos) - 1:
                f.write("\n")
        i+=1
    f.close()
    menu()

def generarReporte():
    print("\n------------------------------REPORTE------------------------------")
    f = open('dispositivos_guardados.txt','r')
    dispositivos = f.readlines()
    f.close()
    print("Elija un dispositivo:\n")
    i=0
    while i<len(dispositivos):
        print(i + 1,".- ",dispositivos[i])
        i+=1
    aux = input()
    opc = int(aux) - 1
    datos = dispositivos[opc].split()
    
    #Consultas
    consulta = consultaSNMP(datos[0],datos[3],"1.3.6.1.2.1.1.1.0")
    if consulta.find("Linux") == 1:
        so = "Linux"
    else:
        so = "Windows"
    nombreDispositivo = consultaSNMP(datos[0],datos[3],"1.3.6.1.2.1.1.5.0")
    contacto = consultaSNMP(datos[0],datos[3],"1.3.6.1.2.1.1.4.0")
    ubicacion = consultaSNMP(datos[0],datos[3],"1.3.6.1.2.1.1.6.0")
    numeroInterfaces = consultaSNMP(datos[0],datos[3],"1.3.6.1.2.1.2.1.0")
    #'1.3.6.1.2.1.2.2.1.7.'
    i = 1
    max = int(0)
    data = [["Interfaz", 'Status']]
    if int(numeroInterfaces)>5 :
        max = 5
    else: 
        max = int(numeroInterfaces)
    while i<=max :
        consultaState = consultaSNMP(datos[0],datos[3],'1.3.6.1.2.1.2.2.1.7.' + str(i))
        consultaAux = consultaSNMP(datos[0],datos[3],"1.3.6.1.2.1.2.2.1.2."+str(i))
        if so != "Linux" :
            consultaDes = bytes.fromhex(consultaAux[3:]).decode('utf-8')
        else:
            consultaDes = consultaAux
        if consultaState[1] == "1":
            data.append([consultaDes,"up"])
        elif consultaState[1] == "2":
            data.append([consultaDes,"down"])
        else :
            data.append([consultaDes,"testing"])
        i+=1
    
    #Generar PDF
    fecha = datetime.today().strftime('%Y_%m_%d_%H_%M_%S')
    nombre = fecha + "_reporteSNMP.pdf"
    doc = canvas.Canvas(nombre)
    doc.setTitle("Reporte SNMP")
    doc.drawString(50, 750, "Administración de Servicios en Red")
    doc.drawString(50, 725, "Práctica 1")
    doc.drawString(50, 700, "Eduardo Cuevas Solorza 4CM13")
    
    doc.drawString(50,600, "Sistema operativo: " + so)
    doc.drawString(50,575, "Nombre del dispositivo: " + nombreDispositivo)
    doc.drawString(50,550, "Contacto: " + contacto)
    doc.drawString(50,525, "Ubicación: " + ubicacion)
    doc.drawString(50,500, "Número de interfaces: " + numeroInterfaces)
    
    width = 400
    height = 1000
    x = 175
    y = 325
    f = Table(data,style=[
                ('GRID',(0,0),(-1,-1),0.5,colors.gray),('ALIGN',(0,0),(1,0),'CENTER')])
    f.wrapOn(doc, width, height)
    f.drawOn(doc, x, y)
    doc.save()
    menu()
def menu():
    print("\n-------------------------------------------------")
    print("Sistema de Administración de Red")
    print("Práctica 1 - Adquisición de Información")
    print("Eduardo Cuevas Solorza 4CM13 2020630095")
    print("-------------------------------------------------\n")
    print("\nElige una opción:")
    print("\n1. Agregar dispositivo")
    print("2. Cambiar información de dispositivo")
    print("3. Eliminar dispositivo")
    print("4. Generar Reporte\n")
    opc = input()

    if opc == "1":
        agregarDispositivo()
    if opc == "2":
        editarDispositivo()
    if opc == "3":
        eliminarDispositivo()
    if opc == "4":
        generarReporte()
    if opc<"4" and opc>"1":
        exit()

def consultaSNMP(comunidad,host,oid):
    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
               CommunityData(comunidad,mpModel=0),
               UdpTransportTarget((host, 161)),
               ContextData(),
               ObjectType(ObjectIdentity(oid))))

    if errorIndication:
        print(errorIndication)
    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(),errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
    else:
        for varBind in varBinds:
            varB=(' = '.join([x.prettyPrint() for x in varBind]))
            resultado= varB.split("=")[1]
    return resultado

menu()
