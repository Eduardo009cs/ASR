import sys
import rrdtool
from  Notify import send_alert_attached
import time
rrdpath = 'RRD/'
imgpath = 'Images/'

ultima_lectura = int(rrdtool.last(rrdpath+"trend.rrd"))
tiempo_final = ultima_lectura
tiempo_inicial = tiempo_final - 1800

def generarGrafica(ultima_lectura,dato,titulo,u1,u2,u3):
    tiempo_final = int(ultima_lectura)
    tiempo_inicial = tiempo_final - 1800
    ret = rrdtool.graphv( imgpath+titulo+".png",
                     "--start",str(tiempo_inicial),
                     "--end",str(tiempo_final),
                     "--vertical-label=Cpu load",
                    '--lower-limit', '0',
                    '--upper-limit', '100',
                    "--title=Carga del " + titulo,
                    "DEF:carga="+rrdpath+"trend.rrd:"+dato+":AVERAGE",
                     "VDEF:cargaMAX=carga,MAXIMUM",
                     "VDEF:cargaMIN=carga,MINIMUM",
                     "VDEF:cargaSTDEV=carga,STDEV",
                     "VDEF:cargaLAST=carga,LAST",
                     "CDEF:umbral"+u1+"=carga,"+u1+",LT,0,carga,IF",
                     "CDEF:umbral"+u2+"=carga,"+u2+",LT,0,carga,IF",
                     "CDEF:umbral"+u3+"=carga,"+u3+",LT,0,carga,IF",
                     "AREA:carga#00FF00:Carga de " + titulo ,
                     "AREA:umbral"+u1+"#00FF00:Carga " + titulo +" mayor de "+u1+"",
                     "AREA:umbral"+u2+"#FF7A00:Carga " + titulo +" mayor de "+u2+"",
                     "AREA:umbral"+u3+"#FF0000:Carga " + titulo +" mayor de "+u3+"",
                     "HRULE:"+u1+"#00FF00:Umbral  "+u1+"%",
                     "HRULE:"+u2+"#FF7A00:Umbral  "+u2+"%",
                     "HRULE:"+u3+"#FF0000:Umbral  "+u3+"%",
                     "PRINT:cargaLAST:%6.2lf",
                     "GPRINT:cargaMIN:%6.2lf %SMIN",
                     "GPRINT:cargaSTDEV:%6.2lf %SSTDEV",
                     "GPRINT:cargaLAST:%6.2lf %SLAST" )
    #print (ret)
pathImage = "Images/useCPU.png"
envioCPU30 = True
envioCPU75 = True
envioCPU80 = True

envioRAM30 = True
envioRAM70 = True
envioRAM80 = True

envioDisco30 = True
envioDisco70 = True
envioDisco90 = True


while (1):
    ultima_actualizacion = rrdtool.lastupdate(rrdpath + "trend.rrd")
    timestamp=ultima_actualizacion['date'].timestamp()
    datoCPU=ultima_actualizacion['ds']["usoCPU"]
    datoRAM=ultima_actualizacion['ds']["usoRAM"]
    datoDisco=ultima_actualizacion['ds']["usoDisco"]
    #print(datoCPU)
    #print(datoRAM)
    #print(datoDisco)
    
    if datoCPU> 80 and envioCPU80:
        pathImage = "Images/CPU.png"
        generarGrafica(int(timestamp),"usoCPU","CPU","30","75","80")
        send_alert_attached("-----NOTIFICACIÓN: USO EXCESIVO CPU-----","El uso del CPU esta por encima del 80%, favor de tomar las medidas correspondientes.",pathImage)
        envioCPU80 = False
        print("Enviado")
    elif datoCPU >75 and envioCPU75:
        pathImage = "Images/CPU.png"
        generarGrafica(int(timestamp),"usoCPU","CPU","30","75","80")
        send_alert_attached("-----NOTIFICACIÓN: USO MODERADO CPU-----","El uso del CPU esta por encima del 75%, favor de monitoriar el uso.",pathImage)
        envioCPU75 = False
        print("Enviado")
    elif datoCPU > 30 and envioCPU30:
        pathImage = "Images/CPU.png"
        generarGrafica(int(timestamp),"usoCPU","CPU","30","75","80")
        envioCPU30 = False
        send_alert_attached("-----NOTIFICACIÓN: USO NORMAL CPU-----","El uso del CPU esta por encima del 30%.",pathImage)
        print("Enviado")
    
    """if datoRAM> 80 and envioRAM80:
        pathImage = "Images/RAM.png"
        generarGrafica(int(timestamp),"usoRAM","RAM","30","70","80")
        send_alert_attached("-----NOTIFICACIÓN: USO EXCESIVO RAM-----","El uso de la RAM esta por encima del 80%, favor de tomar las medidas correspondientes.",pathImage)
        envioRAM80 = False
        print("Enviado")
    elif datoRAM >70 and envioRAM70:
        pathImage = "Images/RAM.png"
        generarGrafica(int(timestamp),"usoRAM","RAM","30","70","80")
        send_alert_attached("-----NOTIFICACIÓN: USO MODERADO RAM-----","El uso de la RAM esta por encima del 70%, favor de monitoriar el uso.",pathImage)
        envioRAM70 = False
        print("Enviado")
    elif datoRAM > 30 and envioRAM30:
        pathImage = "Images/RAM.png"
        generarGrafica(int(timestamp),"usoRAM","RAM","30","70","80")
        envioRAM30 = False
        send_alert_attached("-----NOTIFICACIÓN: USO NORMAL RAM-----","El uso de la RAM esta por encima del 30%.",pathImage)
        print("Enviado")"""

    """if datoDisco> 90 and envioDisco90:
        pathImage = "Images/Disco.png"
        generarGrafica(int(timestamp),"usoDisco","Disco","30","70","90")
        send_alert_attached("-----NOTIFICACIÓN: USO EXCESIVO DISCO-----","El uso del Disco esta por encima del 90%, favor de tomar las medidas correspondientes.",pathImage)
        envioDisco90 = False
        print("Enviado")
    elif datoDisco >70 and envioDisco70:
        pathImage = "Images/Disco.png"
        generarGrafica(int(timestamp),"usoDisco","Disco","30","70","90")
        send_alert_attached("-----NOTIFICACIÓN: USO MODERADO DISCO-----","El uso del Disco esta por encima del 70%, favor de monitoriar el uso del Disco.",pathImage)
        envioDisco70 = False
        print("Enviado")
    elif datoDisco > 30 and envioDisco30:
        pathImage = "Images/Disco.png"
        generarGrafica(int(timestamp),"usoDisco","Disco","30","70","90")
        envioDisco30 = False
        send_alert_attached("-----NOTIFICACIÓN: USO NORMAL DISCO-----","El uso del Disco esta por encima del 30%.",pathImage)
        print("Enviado")"""
    time.sleep(20)