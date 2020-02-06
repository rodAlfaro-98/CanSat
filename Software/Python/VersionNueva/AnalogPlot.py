# Module: AnalogPlot.py
from collections import deque
import serial 
import winsound
from time import sleep
import threading as thread

class AnalogPlot:
	def __init__(self, maxLen,doc):
		#self.port = serial.Serial('COM5', 115200)
		# Linux 
		#self.port = serial.Serial('/dev/tty/USB0', 115200)
		# Windows
		self.port = serial.Serial('COM3', 115200)
		self.temp = deque([0.0]*maxLen)
		self.acel = deque([0.0]*maxLen)
		self.pres = deque([0.0]*maxLen)
		
		self.temperatura = deque([0.0])
		self.presion = deque([0.0])
		self.altura = deque([0.0])
		self.orientacion = deque([0.0])
		self.aceleracion = deque([0.0])
		self.tiempo = deque([0])
		
		self.maxLen = maxLen
		self.write = deque("")
		self.doc = doc
		
		self.data = thread.Thread(target=self.getData, args=())
		self.writeIn = thread.Thread(target=self.writeInDoc, args=())
		
		self.startThread()
		

	"""
		@brief Función que agrega los datos a la cola que le corresponde
		@param La cola que sirve como buffer y el valor a ingresar
	"""
	def addToBuf(self, buf, val):
		if len(buf) < self.maxLen:
			buf.append(val)
		else:
			buf.popleft()
			buf.append(val)

	"""
		@brief Función que activadora de addToBuf
		@param Dato a ingresar
	"""
	def add(self, data):
		self.addToBuf(self.temp, data[0])
		self.addToBuf(self.pres, data[1])
		self.addToBuf(self.acel, data[4])
		
		self.temperatura.append(data[0])
		self.presion.append(data[1])
		self.altura.append(data[2])
		self.orientacion.append(data[3])
		self.aceleracion.append(data[4])
		self.tiempo.append(int(data[5]))

	"""
		@brief Función que obtiene los datos del puerto para actualizarlos en la gráfica e ingresarlos al documento
		@param Las gráficas a actualizar
	"""
	def update(self, frameNum, a0, a1, a2, a3):
		try:	
			a0.set_data(range(self.maxLen), self.temp)
			a1.set_data(range(self.maxLen), self.acel)
			a2.set_data(range(self.maxLen), self.pres)
			a3.set_data(self.orientacion.popleft(),2)
			return a0,
		except:
			pass
		finally:
			pass
			#f.close()
			
			
	def setDoc(self,doc):
		self.doc = doc
		
	def writeInDoc(self):
		i=0
		while self.writing:
			sleep(0.25)
			print('escribiendo '+str(i))
			f = open('Datos{}.txt'.format(self.doc), 'a')
			f.write(str(self.temperatura.popleft())+','+str(self.presion.popleft())+','+str(self.altura.popleft())+','+str(self.orientacion.popleft())+','+str(self.aceleracion.popleft())+','+str(self.tiempo.popleft())+'\n')
			f.close()
			i+=1
		self.writeIn.should_abort_immediately = True
		
	def getData(self):
		i = 0
		while self.getin:
			print('getin '+str(i))
			ln = self.port.readline()
			line = str(ln.decode("utf-8"))
			data = [float(val) for val in line.split(',')]
			self.add(data)
			self.orientacion.append(data[3])
			i+=1
		self.port.close()
		self.data.should_abort_immediately = True
	
	def plot(self):
		pass
		
	def startThread(self):
		self.getin = True
		self.writing = True
		self.data.start()
		sleep(5)
		self.writeIn.start()
		
	def finishThread(self):
		self.getin = False
		self.writing = False
		