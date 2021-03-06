#from construct import *
import struct
import serial
from bitarray import bitarray
import signal
import sys
ser = serial.Serial(
    port='/dev/ttyUSB0',\
    baudrate=115200,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
        timeout=0) ## connecting to laser module
        
        
def signal_handler(signal, frame): ## closing on end
        print('You pressed Ctrl+C!')
        ser.close()
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

errors={16370:"no object detected",16372: "too close to sensor",16374: "too far from sensor",16376: "object cannot be evaluated", 16378: "external laser off"} ## error detection
while True:
        for c in ser.read():
            komunikat=bitarray(endian='big')
            komunikat.frombytes(c)
            
            try:
                if komunikat[0]:
                    d =ser.read(1)
                    komunikat.frombytes(d)
                    
                    
                    f=bitarray([False,False],endian='big')

                    f=f+komunikat[1:8]+komunikat[9:]

                    digital_output=struct.unpack('>H',f.tobytes())[0]
                    #print digital_output
                    if digital_output not in errors:
                        final=(digital_output*1.02/16368.0-0.01)*200
                        print "wyliczone",final
                    else:
                        print errors[digital_output]
            except:
                print "no data to show"
ser.close()
