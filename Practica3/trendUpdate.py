import time
import rrdtool
from getSNMP import consultaSNMP
rrdpath = 'RRD/'
carga_CPU = 0
ramTotal = 0
ramUsada = 0
discoTotal = 0
discoUsado = 0
ramPorcentaje = 0
discoPorcentaje = 0

while 1:
    carga_CPU1 = int(consultaSNMP('gustavoRomero','localhost','1.3.6.1.2.1.25.3.3.1.2.5'))
    carga_CPU2 = int(consultaSNMP('gustavoRomero','localhost','1.3.6.1.2.1.25.3.3.1.2.6'))
    discoTotal = 4096*int(consultaSNMP('gustavoRomero','localhost','1.3.6.1.2.1.25.2.3.1.5.1'))
    discoUsado = 4096*int(consultaSNMP('gustavoRomero','localhost','1.3.6.1.2.1.25.2.3.1.6.1'))
    ramTotal = 65536*int(consultaSNMP('gustavoRomero','localhost','1.3.6.1.2.1.25.2.3.1.5.3'))
    ramUsada = 65536*int(consultaSNMP('gustavoRomero','localhost','1.3.6.1.2.1.25.2.3.1.6.3'))
    
    carga_CPUs = (carga_CPU1 + carga_CPU2)/2
    ramPorcentaje = (ramUsada * 100)/ramTotal
    discoPorcentaje = (discoUsado * 100)/discoTotal
    ramPorcentaje = round(ramPorcentaje,2)
    discoPorcentaje = round(discoPorcentaje,2) 
    
    valor = "N:" + str(carga_CPUs) + ":" + str(ramPorcentaje) + ":" + str(discoPorcentaje)
    print (valor)
    rrdtool.update(rrdpath+'trend.rrd', valor)
    rrdtool.dump(rrdpath+'trend.rrd',rrdpath+'trend.xml')
    time.sleep(5)

if ret:
    print (rrdtool.error())
    time.sleep(300)