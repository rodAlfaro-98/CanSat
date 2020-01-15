
import serial, time

port="/dev/ttyACM0"
bauds=9600
lat =[]                       # empty list to store the data
lon=[]

arduino = serial.Serial(port,bauds)
time.sleep(2)


for i in range(10):
    b = arduino.readline()     
    print(b)
    string = b.rstrip()
    lis=string.split(",")
    

    lat.append(lis[0])
    lon.append(lis[1])           # add to the end of data list
    time.sleep(0.1)            # wait (sleep) 0.1 seconds



arduino.close()

print "lat:"
print lat
print "lon:"
print lon