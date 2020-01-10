#Funcional
import serial 
#import winsound
import Tkinter as tk 
from collections import deque
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from GraficaTxt import GText

doc = 0
estado = 1

def NewFile():
	with open('Datos.txt','w') as f:
		f.write('')

plt.style.use('seaborn')
fig = Figure()
ax = fig.add_subplot(221)
ay = fig.add_subplot(222)
az = fig.add_subplot(223)
aw = fig.add_subplot(224, projection = 'polar')
#fig.suptitle('CanSat')

ax.set_title('Temperatura')
ax.set_xlim(0,5) 
ax.set_ylim(10,40)

ay.set_title('Aceleracion')
ay.set_xlim(0,5)
ay.set_ylim(-15,50)

az.set_ylabel('Presion')
az.set_xlim(0,5)
az.set_ylim(760,800)

a0, = ax.plot([],[],'r-')
a1, = ay.plot([],[],'g-')
a2, = az.plot([],[],'m-')
a3, = aw.plot(0,2,'co')


class AnalogPlot:
	def __init__(self, maxLen):
		self.port = serial.Serial('COM4', 115200)
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
			f = open('Datos.txt', 'a')
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

		contenedor = tk.Frame(self)
		contenedor.pack(side='top', fill='both', expand= True)
		contenedor.grid_rowconfigure(0, weight = 1)
		contenedor.grid_columnconfigure(0, weight = 1)

		frame = GraphLive(contenedor, self)
		frame.grid(row=0, column=0, sticky='nsew')
		frame.tkraise()

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

	def finish(self):
		try:
			analogPlot.port.close()
			estado = 0
		except:
			pass

class GraphLive(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)

		presLabel = tk.Label(self, text="equipo ad infinitum", bg='#e1c0e4',
					font=('Copperplate Gothic Light', 18))
		presLabel.grid(row=0, column=0, columnspan=4, sticky='nsew')

		RestartButton = tk.Button(self, text='Restart', fg='green',command=lambda:controller.restart())
		RestartButton.grid(row=1, column=0, sticky='nsew')

		GrapxButton = tk.Button(self, text='Graph.txt', command=lambda:GText('Datos.txt'))
		GrapxButton.grid(row=1, column=1, sticky='nsew')

		FinButton = tk.Button(self, text='Finish', fg='red', command=lambda:controller.finish())
		FinButton.grid(row=1, column=2, sticky='nsew')

		canvas = FigureCanvasTkAgg(fig, self)
		canvas.draw()
		canvas.get_tk_widget().grid(row=2, column=0, columnspan=3)#pack(side='top', fill='both', expand=True)

NewFile()

if __name__ == '__main__':

	app = Aplicacion()
	#app.geometry('800x797')
	try:
		if estado != 0:
			analogPlot = AnalogPlot(4)
			anim = animation.FuncAnimation(fig, analogPlot.update, fargs=(a0, a1, a2, a3), interval=50)
	except:
		pass
	app.mainloop()

