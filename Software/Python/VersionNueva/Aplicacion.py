# Module: Aplicacion.py
import tkinter as tk
import AnalogPlot
from matplotlib.figure import Figure
import matplotlib.animation as animation
import GraphLive as grphlive
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from GraficaTxt_2 import GText

class Aplicacion(tk.Tk):
	doc = 0
	analogPlot = None

	def __init__(self,fig):
		tk.Tk.__init__(self)
		self.wm_title('CanSat App')
		self.resizable(width=False,height=False)
		self.init_window()

		contenedor = tk.Frame(self)
		contenedor.pack(side='top', fill='both', expand= True)
		contenedor.grid_rowconfigure(0, weight = 1)
		contenedor.grid_columnconfigure(0, weight = 1)

		frame = grphlive.GraphLive(contenedor, self, fig)
		frame.grid(row=0, column=0, sticky='nsew')
		frame.tkraise()
		self.NewFile()
		self.doc = 0
	
	"""
		@brief Función que inicializa la ventana de grafiación
	"""
	def init_window(self):
		menu = tk.Menu(self)
		self.config(menu=menu)

		#Creación del menú, los botonoes son representados por labels y las acciones son las funciones lambda
		file = tk.Menu(menu)
		file.add_command(label='Start', command = lambda:self.start())
		file.add_command(label='Restart', command = lambda:self.restart())
		file.add_command(label='Finish', command = lambda:self.finish())
		file.add_command(label='Exit', command = lambda:exit())
		menu.add_cascade(label = 'File', menu = file)

		
		Graphs = tk.Menu(menu)
		Graphs.add_command(label='All', command = lambda:GText(self.doc,'all'))
		Graphs.add_command(label='Altura', command = lambda:GText(self.doc,'a'))
		Graphs.add_command(label='Presion', command = lambda:GText(self.doc,'p'))
		Graphs.add_command(label='Temperatura', command = lambda:GText(self.doc,'t'))
		Graphs.add_command(label='Aceleracion', command = lambda:GText(self.doc,'c'))
		menu.add_cascade(label = 'Graphs', menu = Graphs)

	"""
		@brief Función que se encarga de reiniciar el procesa de graficación
	"""
	def restart(self):
		self.doc+=1
		try:
			self.analogPlot.stopThread()
			self.analogPlot.port.close()
			self.NewFile()
			self.analogPlot.port.open()
			self.alaogPort.setDoc(self.doc)
			self.analogPlot.startThread()
		except:
			self.NewFile()
			#pass
		#finally:
			#winsound.PlaySound('ConexionLista', winsound.SND_FILENAME)

	"""
		@brief Función que cambia el estado de la aplicación para que inicie el proceso de la graficación
	"""
	def start(self):
		self.estado = True
		if(self.analogPlot != None):
			self.analogPlot.startThread()
		return True

	"""
		@brief Función que se encarga de reiniciar el procesa de graficación
	"""
	def finish(self):
		global estado
		try:
			self.analogPlot.finishThread()
			self.estado = False
		except:
			pass
	
	def getEstado(self):
		return self.estado
	
	"""
		@brief Función que permite la apertura de un nuevo archivo
	"""
	def NewFile(self):
		with open('Datos{}.txt'.format(self.doc),'w') as f:
			f.write('')
			f.close()
			
	def setAnalogPlot(self, analogPlot):
		self.analogPlot = analogPlot
		self.analogPlot.setDoc(self.doc)