# Module: AnalogPlot.py
from collections import deque
import serial 
import winsound

class AnalogPlot:
	def __init__(self, maxLen):
		#self.port = serial.Serial('COM5', 115200)
		# Linux 
		#self.port = serial.Serial('/dev/tty/USB0', 115200)
		# Windows
		self.port = serial.Serial('COM3', 115200)
		self.temp = deque([0.0]*maxLen)
		self.acel = deque([0.0]*maxLen)
		self.pres = deque([0.0]*maxLen)
		self.orientacion = deque([0.0])
		self.maxLen = maxLen
		self.write = deque("")

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

	"""
		@brief Función que obtiene los datos del puerto para actualizarlos en la gráfica e ingresarlos al documento
		@param Las gráficas a actualizar
	"""
	def update(self, frameNum, a0, a1, a2, a3):
		try:
			#line = self.data.popleft()
			#if len(data) == 6:
				#self.add(data)
			"""ln = self.port.readline()
			line = str(ln.decode("utf-8"))
			data = [float(val) for val in line.split(',')]
			self.add(data)"""
			
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
		while True:
			if(len(self.write)>5):
				i=0
				size=len(self.write)
				while(i<size):
					f = open('Datos{}.txt'.format(self.doc), 'a')
					line = self.write.popleft()
					#print(line)
					f.write(line)
					i+=1
					f.close()
		
	def getData(self):
		while(True):
			ln = self.port.readline()
			line = str(ln.decode("utf-8"))
			data = [float(val) for val in line.split(',')]
			self.add(data)
			self.orientacion.append(data[3])
			self.write.append(line)
	
	def plot(self):
		pass