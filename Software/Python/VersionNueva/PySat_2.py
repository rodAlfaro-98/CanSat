#Funcional
import serial 
import winsound
import tkinter as tk
from collections import deque
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from GraficaTxt_2 import GText
from time import sleep
import sys
import _thread as thread

# Importamos modulos propios
import AnalogPlot as anaplt
import Aplicacion as apk

global estado
estado = True

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

if __name__ == '__main__':
	app = apk.Aplicacion(fig)
	app.start()
	#try:
	if app.getEstado():
		print("Ajua")
		analogPlot = anaplt.AnalogPlot(10,app.doc)
		app.setAnalogPlot(analogPlot)
		#thread.start_new_thread(app.analogPlot.getData,())
		anim = animation.FuncAnimation(fig, app.analogPlot.update, fargs=(a0, a1, a2, a3), interval=1)
		sleep(5)
		#thread.start_new_thread(app.analogPlot.writeInDoc,())
	#except:
		#print("Qiubo")
		#sys.exit()
	app.mainloop()

