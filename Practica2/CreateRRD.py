import rrdtool
ret = rrdtool.create("base.rrd",
                     "--start",'N',
                     "--step",'60',
                     "DS:paquetesUnicast:COUNTER:120:U:U",
                     "DS:paquetesIPv4:COUNTER:120:U:U",
                     "DS:mensajesICMPe:COUNTER:120:U:U",
                     "DS:segmentosRecibidos:COUNTER:120:U:U",
                     "DS:datagramasEnt:COUNTER:120:U:U",
                     "RRA:AVERAGE:0.5:10:500",
                     "RRA:AVERAGE:0.5:1:1500")
rrdtool.dump('base.rrd','traficoRED.xml')
if ret:
    print (rrdtool.error())