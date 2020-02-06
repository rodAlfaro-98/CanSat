# Module GraphLive
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class GraphLive(tk.Frame):
	def __init__(self, parent, controller, fig):
		tk.Frame.__init__(self, parent)

		presLabel = tk.Label(self, text="equipo ad infinitum", bg='#e1c0e4',
					font=('Copperplate Gothic Light', 18))
		presLabel.grid(row=0, column=0, sticky='nsew')

		canvas = FigureCanvasTkAgg(fig, self)
		canvas.draw()
		canvas.get_tk_widget().grid(row=1, column=0)
