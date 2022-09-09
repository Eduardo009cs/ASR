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
    dispositivos = f.read()
    dispositivo = []
    for aux in dispositivos.split("\n"):
        dispositivo.append(aux)
    print("Elija un dispositivo entre 1 y", len(dispositivo) - 1)
    opc = input()
    op =int(opc)
    dis=[]
    for aux2 in dispositivo[op-1].split(" "):
        dis.append(aux2)
    print(dis[0])
    dis[0] = input("Comunidad: ")
    dis[1] = input("Version SNMP: ")
    dis[2] = input("Puerto: ")
    dis[3] = input("IP: ")
    outfile =  open('dispositivos_guardados.txt','w')
    i = 0
    print(dispositivo[op-1])
    dispositivo[op-1][0]  = dis[0]
    dispositivo[op-1][1]  = dis[1]
    dispositivo[op-1][2]  = dis[2]
    dispositivo[op-1][3]  = dis[3]
    for i in range(len(dispositivo)):
        outfile.write(dispositivo[i])
        outfile.write("\n")
    outfile.close()
    
def eliminarDispositivo():
    print("Eliminar dispositivo")
    
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
