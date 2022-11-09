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
import rrdtool
import sys
import time
import threading

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
    
    print("Escriba la fecha incial (Y/m/d H:M:S):")
    fechaInicial = input()
    print("Escriba la fecha final (Y/m/d H:M:S):")
    fechaFinal = input()
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
    tiempo_final =  int(datetime.strptime(fechaFinal, "%Y/%m/%d %H:%M:%S").timestamp())
    tiempo_inicial = int(datetime.strptime(fechaInicial, "%Y/%m/%d %H:%M:%S").timestamp())
    graficar("paquetesUnicast", tiempo_inicial, tiempo_final,"0000FF")
    graficar("paquetesIPv4", tiempo_inicial, tiempo_final,"00F0FF")
    graficar("mensajesICMPe", tiempo_inicial, tiempo_final,"F000F0")
    graficar("segmentosRecibidos", tiempo_inicial, tiempo_final,"FF0F00")
    graficar("datagramasEnt", tiempo_inicial, tiempo_final,"0FFF00")
    fecha = datetime.today().strftime('%Y_%m_%d_%H_%M_%S')
    fecha2 = datetime.today().strftime('%d %m %Y %H:%M:%S')
    nombre = fecha + "_reporteSNMP.pdf"
    doc = canvas.Canvas(nombre)
    doc.setTitle("Reporte SNMP")
    doc.drawString(50, 770, "version: 1")
    doc.drawString(50, 750, "device: agent1")
    doc.drawString(50, 730, "description: Accounting Agent 1")
    doc.drawString(50, 710, "date: " + fecha2)
    doc.drawString(50, 690, "defaultProtocol: radius ")

    doc.drawString(50, 660, "rdate: " + fecha2)
    doc.drawString(50, 640, "#NAS-IP-Address ")
    doc.drawString(50, 620, "4:" + datos[3])
    doc.drawString(50, 600, "#NAS-Port")
    doc.drawString(50, 580, "5:12")
    doc.drawString(50, 560, "#NAS-Port-Type")
    doc.drawString(50, 540, "61:2")
    doc.drawString(50, 520, "#User-Name")
    doc.drawString(50, 500, "1:"+contacto)
    doc.drawString(50, 480, "#Acct-Status-Type ")
    doc.drawString(50, 460, "40:2")
    doc.drawString(50, 440, "#Acct-Delay-Time ")
    doc.drawString(50, 420, "41:14")
    doc.drawString(50, 400, "#Acct-Input-Octets")
    doc.drawString(50, 380, "42:" + consultaSNMP(datos[0], datos[3], "1.3.6.1.2.1.2.2.1.10.10"))
    doc.drawString(50, 360, "#Acct-Output-Octets")
    doc.drawString(50, 340, "43:" +  consultaSNMP(datos[0], datos[3], "1.3.6.1.2.1.2.2.1.16.10"))
    doc.drawString(50, 320, "#Acct-Session-Id ")
    doc.drawString(50, 300, "44:1")
    doc.drawString(50, 280, "#Acct-Authentic")
    doc.drawString(50, 260, "45:1")
    doc.drawString(50, 240, "#Acct-Session-Time ")
    doc.drawString(50, 220, "46:127")
    doc.drawString(50, 200, "#Acct-Input-Packets")
    doc.drawString(50, 180, "47:" + consultaSNMP(datos[0], datos[3], "1.3.6.1.2.1.2.2.1.11.10"))
    doc.drawString(50, 160, "#Acct-Output-Packets ")
    doc.drawString(50, 140, "48:" +  consultaSNMP(datos[0], datos[3], "1.3.6.1.2.1.2.2.1.17.10"))
    doc.drawString(50, 120, "#Acct-Terminate-Cause")
    doc.drawString(50, 100, "49:10")
    doc.drawString(50, 80, "#Acct-Multi-Session-Id")
    doc.drawString(50, 60, "50:73")
    doc.drawString(50, 40, "#Acct-Link-Count")
    doc.drawString(50, 20, "51:2")
    
    doc.showPage()
    doc.drawInlineImage( "./paquetesUnicast.png", 50, 700, 250, 100)
    doc.drawInlineImage( "./paquetesIPv4.png", 325, 700, 250, 100)
    doc.drawInlineImage( "./mensajesICMPe.png", 50, 550, 250, 100)
    doc.drawInlineImage( "./segmentosRecibidos.png", 325, 550, 250, 100)
    doc.drawInlineImage( "./datagramasEnt.png", 50, 400, 250, 100)
    

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
def graficar(valor, tiempo_inicial, tiempo_final,color):
    
    ret = rrdtool.graphv( valor +".png",
                        "--start",str(tiempo_inicial),
                        "--end",str(tiempo_final),
                        "DEF:datos=base.rrd:" + valor +":AVERAGE",
                        "LINE3:datos#" + color + ":"+ valor)


menu()

#paquetes unicast recibidos 1.3.6.1.2.1.2.11.0
#paquetes recibidos a protocolos IPv4 1.3.6.1.2.1.4.3.0
#Mensajes ICMPecho enviados
#Segmentos recibidos
#Datagramas entregados