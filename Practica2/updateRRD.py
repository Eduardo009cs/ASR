import time
import rrdtool
from getSNMP import consultaSNMP
total_input_traffic = 0
total_output_traffic = 0

while 1:
    paqutesUnicast = int(
        consultaSNMP('eduardoCuevas','172.20.10.7',
                     '1.3.6.1.2.1.2.2.1.11.3'))
    paquetesIPv4 = int(
        consultaSNMP('eduardoCuevas','172.20.10.7',
                     '1.3.6.1.2.1.4.3.0'))
    mensajesICMPe = int(
        consultaSNMP('eduardoCuevas','172.20.10.7',
                     '1.3.6.1.2.1.5.8.0'))
    segmentosRecibidos = int(
        consultaSNMP('eduardoCuevas','172.20.10.7',
                     '1.3.6.1.2.1.6.10.0'))
    datagramasEntregados = int(
        consultaSNMP('eduardoCuevas','172.20.10.7',
                     '1.3.6.1.2.1.4.3.0'))
    valor = "N:" + str(paqutesUnicast) + ':' + str(paquetesIPv4) + ':' + str(mensajesICMPe) + ':' + str(segmentosRecibidos) + ':' + str(datagramasEntregados)
    print (valor)
    rrdtool.update('base.rrd', valor)
    rrdtool.dump('base.rrd','traficoRED.xml')
    time.sleep(1)

if ret:
    print (rrdtool.error())
    time.sleep(300)