#Funcional
import serial 
#import winsound
import tkinter as tk
#import Tkinter as tk
from collections import deque
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from GraficaTxt import GText

doc = 0
global estado
estado = True

def NewFile():
	with open('Datos{}.txt'.format(doc),'w') as f:
		f.write('')

plt.style.use('seaborn')
fig = Figure()
fig.set_tight_layout(tight = 'True')

ax = fig.add_subplot(221)
ax.set_title('Temperatura')
ax.set_xlim(0,5) 
ax.set_ylim(10,40)

ay = fig.add_subplot(222)
ay.set_title('Aceleracion')
ay.set_xlim(0,5)
ay.set_ylim(-15,50)

az = fig.add_subplot(223)
az.set_title('Presion')
az.set_xlim(0,5)
az.set_ylim(760,800)

aw = fig.add_subplot(224, projection = 'polar')
aw.set_title('Orientacion', loc='left')

a0, = ax.plot([],[],'r-')
a1, = ay.plot([],[],'g-')
a2, = az.plot([],[],'m-')
a3, = aw.plot(0,2,'co')

#plt.subplots_adjust(hspace=0.90,wspace=0.90)


class AnalogPlot:
	def __init__(self, maxLen):
		#self.port = serial.Serial('COM5', 115200)
		self.port = serial.Serial('/dev/tty/USB0', 115200)
		self.temp = deque([0.0]*maxLen)
		self.acel = deque([0.0]*maxLen)
		self.pres = deque([0.0]*maxLen)
		self.maxLen = maxLen

	def addToBuf(self, buf, val):
		if len(buf) < self.maxLen:
			buf.append(val)
		else:
			buf.popleft()
			buf.append(val)

	def add(self, data):
		self.addToBuf(self.temp, data[0])
		self.addToBuf(self.pres, data[1])
		self.addToBuf(self.acel, data[4])

	def update(self, frameNum, a0, a1, a2, a3):
		try:
			f = open('Datos{}.txt'.format(doc), 'a')
			ln = self.port.readline()
			line = str(ln.decode("utf-8"))
			data = [float(val) for val in line.split(',')]
			if len(data) == 6:
				f.write(line)
				self.add(data)
				a0.set_data(range(self.maxLen), self.temp)
				a1.set_data(range(self.maxLen), self.acel)
				a2.set_data(range(self.maxLen), self.pres)
				a3.set_data(data[3],2)
				return a0,
		except:
			pass
		finally:
			f.close()

class Aplicacion(tk.Tk):
	def __init__(self):
		tk.Tk.__init__(self)
		self.wm_title('CanSat App')
		self.resizable(width=False,height=False)
		self.init_window()

		contenedor = tk.Frame(self)
		contenedor.pack(side='top', fill='both', expand= True)
		contenedor.grid_rowconfigure(0, weight = 1)
		contenedor.grid_columnconfigure(0, weight = 1)

		frame = GraphLive(contenedor, self)
		frame.grid(row=0, column=0, sticky='nsew')
		frame.tkraise()
	
	def init_window(self):
		menu = tk.Menu(self)
		self.config(menu=menu)

		file = tk.Menu(menu)
		file.add_command(label='Start', command = lambda:self.start())
		file.add_command(label='Restart', command = lambda:self.restart())
		file.add_command(label='Finish', command = lambda:self.finish())
		file.add_command(label='Exit', command = lambda:exit())
		menu.add_cascade(label = 'File', menu = file)

		Graphs = tk.Menu(menu)
		Graphs.add_command(label='All', command = lambda:GText(doc,'all'))
		Graphs.add_command(label='Altura', command = lambda:GText(doc,'a'))
		Graphs.add_command(label='Presion', command = lambda:GText(doc,'p'))
		Graphs.add_command(label='Temperatura', command = lambda:GText(doc,'t'))
		Graphs.add_command(label='Aceleracion', command = lambda:GText(doc,'c'))
		menu.add_cascade(label = 'Graphs', menu = Graphs)

	def restart(self):
		global doc
		doc+=1
		try:
			analogPlot.port.close()
			NewFile()
			analogPlot.port.open()
		except:
			pass
		#finally:
			#winsound.PlaySound('ConexionLista', winsound.SND_FILENAME)

	def start(self):
		global estado
		estado = True

	def finish(self):
		global estado
		try:
			analogPlot.port.close()
			estado = False
		except:
			pass

class GraphLive(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)

		presLabel = tk.Label(self, text="equipo ad infinitum", bg='#e1c0e4',
					font=('Copperplate Gothic Light', 18))
		presLabel.grid(row=0, column=0, sticky='nsew')

		canvas = FigureCanvasTkAgg(fig, self)
		canvas.draw()
		canvas.get_tk_widget().grid(row=1, column=0)

NewFile()

if __name__ == '__main__':
	app = Aplicacion()
	try:
		if estado:
			print("Ajua")
			analogPlot = AnalogPlot(4)
			anim = animation.FuncAnimation(fig, analogPlot.update, fargs=(a0, a1, a2, a3), interval=50)
	except:
		print("Qiubo")
	app.mainloop()

