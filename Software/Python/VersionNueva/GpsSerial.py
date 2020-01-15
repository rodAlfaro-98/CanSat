
import serial, time

port="/dev/ttyACM0"
bauds=115200
lat =[]                       # empty list to store the data
lon=[]

arduino = serial.Serial(port,bauds)
time.sleep(2)

#durante 10 segundos registra la longitud y latitud 
for i in range(10):
    b = arduino.readline()     
    print(b)
    string = b.rstrip()
    lis=string.split(",")
    print lis

    lat.append(lis[0])
    lon.append(lis[1])           # add to the end of data list
    time.sleep(0.1)            # wait (sleep) 0.1 seconds



arduino.close()
#al final regresa un registro de coordenadas
print "lat:"
print lat
print "lon:"
print lon