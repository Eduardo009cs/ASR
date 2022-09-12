#EduardoCuevasSolorza s
from email.policy import default

from pysnmp.hlapi import *
import json

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

    
def menu():
    print("\n-------------------------------------------------")
    print("Sistema de Administración de Red")
    print("Práctica 1 - Adquisición de Información")
    print("Eduardo Cuevas Solorza 4CM13 2020630095")
    print("-------------------------------------------------\n")
    print("\nElige una opción:")
    print("\n1. Agregar dispositivo")
    print("2. Cambiar información de dispositivo")
    print("3. Eliminar dispositivo\n")
    opc = input()

    if opc == "1":
        agregarDispositivo()
    if opc == "2":
        editarDispositivo()
    if opc == "3":
        eliminarDispositivo()
    if opc<"3" and opc>"1":
        exit()

def consultaSNMP(comunidad,host,oid):
    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
               CommunityData(comunidad),
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
            resultado= varB.split()[2]
    return resultado

menu()
