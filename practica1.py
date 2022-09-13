#EduardoCuevasSolorza s
from email.policy import default
from reportlab.pdfgen import canvas
from reportlab.platypus import (SimpleDocTemplate, PageBreak, Image, Spacer,
Paragraph, Table, TableStyle)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from pysnmp.hlapi import *


width, height = A4
def coord(x, y, unit=1):
    x, y = x * unit, height -  y * unit
    return x, y
def agregarDispositivo():
    print("\n---------------AGREGAR---------------")
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
    print("\n---------------EDITAR---------------")
    f = open('dispositivos_guardados.txt','r')
    #dispositivos = f.read()
    dispositivos = f.readlines()
    f.close()
    print("Elija un dispositivo entre el 1 al", len(dispositivos))
    aux = input()
    opc = int(aux) - 1
    print(dispositivos[opc])
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

    

def eliminarDispositivo():
    print("Eliminar dispositivo")
    f = open('dispositivos_guardados.txt','r')
    #dispositivos = f.read()
    dispositivos = f.readlines()
    f.close()
    print("Elija un dispositivo para eliminar entre el 1 al", len(dispositivos))
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

def generarReporte():
    f = open('dispositivos_guardados.txt','r')
    dispositivos = f.readlines()
    f.close()
    print("Elija un dispositivo para eliminar entre el 1 al", len(dispositivos))
    aux = input()
    opc = int(aux) - 1
    datos = dispositivos[opc].split()
    
    #Consultas
    consulta = consultaSNMP(datos[0],datos[3],"1.3.6.1.2.1.1.1.0")
    if consulta.find("Linux") == 1:
        so = "Linux"
    else:
        so = "Windows"
    nombre = consultaSNMP(datos[0],datos[3],"1.3.6.1.2.1.1.5.0")
    contacto = consultaSNMP(datos[0],datos[3],"1.3.6.1.2.1.1.4.0")
    ubicacion = consultaSNMP(datos[0],datos[3],"1.3.6.1.2.1.1.6.0")
    numeroInterfaces = consultaSNMP(datos[0],datos[3],"1.3.6.1.2.1.2.1.0")
    #'1.3.6.1.2.1.2.2.1.7.'
    i = 1
    
    data = [["Interfaz", 'Status']]
    while i<=5 :
        consultaState = consultaSNMP(datos[0],datos[3],'1.3.6.1.2.1.2.2.1.7.' + str(i))
        consultaDes = consultaSNMP(datos[0],datos[3],"1.3.6.1.2.1.2.2.1.2."+str(i))
        if consultaState[1] == "1":
            data.append([consultaDes,"up"])
        elif consultaState[1] == "2":
            data.append([consultaDes,"down"])
        else :
            data.append([consultaDes,"testing"])
        i+=1
    
    #Generar PDF
    
    doc = canvas.Canvas("reporteSNMP.pdf")
    doc.setTitle("Reporte SNMP")
    doc.drawString(50, 750, "Administración de Servicios en Red")
    doc.drawString(50, 725, "Práctica 1")
    doc.drawString(50, 700, "Eduardo Cuevas Solorza 4CM13")
    
    doc.drawString(50,600, "Sistema operativo: " + so)
    doc.drawString(50,575, "Nombre del dispositivo: " + nombre)
    doc.drawString(50,550, "Contacto: " + contacto)
    doc.drawString(50,525, "Ubicación: " + ubicacion)
    doc.drawString(50,500, "Número de interfaces: " + numeroInterfaces)
    
    width = 400
    height = 100
    x = 50
    y = 200
    f = Table(data)
    f.wrapOn(doc, width, height)
    f.drawOn(doc, x, y)
    doc.save()
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
