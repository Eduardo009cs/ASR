import rrdtool
ret = rrdtool.create("RRD/trend.rrd",
                     "--start",'N',
                     "--step",'60',
                     "DS:usoCPU:GAUGE:60:0:100",
                     "DS:usoRAM:GAUGE:60:0:100",
                     "DS:usoDisco:GAUGE:60:0:100",
                     "RRA:AVERAGE:0.5:1:24")
if ret:
    print (rrdtool.error())