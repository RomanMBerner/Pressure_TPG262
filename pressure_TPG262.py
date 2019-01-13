# ///////////////////////////////////////////////////////////////// //
#                                                                   //
# python script to read the pressure with a                         //
# Pfeiffer Vacuum Dual Gauge TPG 262 (261) Controller, PTG28280     //
#                                                                   //
# From the serial output, put a NullModem before connecting         //
# to the Ser232->USB converter (see datasheet p.23)                 //
#                                                                   //
# Last modifications: 13.01.2019 by R.Berner                        //
#                                                                   //
# ///////////////////////////////////////////////////////////////// //

from   class_def import *
import subprocess
import time

# Setting up connection
print "Setting up connection"
gauge = TPG262(port='/dev/ttyUSB1')

# Acquiring data
while 1:
    gauge._send_command('PRX')
    answer = gauge._get_data()
    # The answer is of the form: statusCode1,pressure1,statusCode2,pressure2
    statusCode_p1 = int(answer.split(',')[0])
    p1 = float(answer.split(',')[1])
    statusCode_p2 = int(answer.split(',')[2])
    p2 = float(answer.split(',')[3])

    # Send data to database (only if data is of good quality, e.g. statusCode==0)
    if statusCode_p1==0 and p1>=0.:
        print "p1 =", p1, gauge.pressure_unit()
        post1_bar = "pressure_bar,sensor=1,pos=outer_bath value=" + str(p1)
        subprocess.call(["curl", "-i", "-XPOST", "lhepdaq2.unibe.ch:8086/write?db=module_zero_run_jan2019", "--data-binary", post1_bar])
    if statusCode_p1==1: print "Sensor 1: Underrange"
    if statusCode_p1==2: print "Sensor 1: Overrange"
    if statusCode_p1==3: print "Sensor 1: Sensor error"
    if statusCode_p1==4: print "Sensor 1: Sensor off"
    if statusCode_p1==5: print "Sensor 1: No sensor (output: 5,20000E-2 [mbar])"
    if statusCode_p1==6: print "Sensor 1: Identification error"

    if statusCode_p2==0 and p2>=0.:
        print "p2 =", p2, gauge.pressure_unit()
        post2_bar = "pressure_bar,sensor=2,pos=outer_bath value=" + str(p2)
        subprocess.call(["curl", "-i", "-XPOST", "lhepdaq2.unibe.ch:8086/write?db=module_zero_run_jan2019", "--data-binary", post2_bar])
    if statusCode_p2==1: print "Sensor 2: Underrange"
    if statusCode_p2==2: print "Sensor 2: Overrange"
    if statusCode_p2==3: print "Sensor 2: Sensor error"
    if statusCode_p2==4: print "Sensor 2: Sensor off"
    if statusCode_p2==5: print "Sensor 2: No sensor (output: 5,20000E-2 [mbar]"
    if statusCode_p2==6: print "Sensor 2: Identification error"

    time.sleep(0.95)
