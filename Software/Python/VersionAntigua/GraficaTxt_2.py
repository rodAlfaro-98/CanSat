
import matplotlib.pyplot as plt 

def GText(n,g):
	temp = []
	pres = []
	altt = []
	orin = []
	acel = []
	time = []

	file = open('Datos{}.txt'.format(n), 'r')
	dataArray = file.read()
	datas = dataArray.split('\n')
	for line in datas:
		if len(line)>1:
			t,p,a,o,g,m = line.split(',')
			temp.append(float(t))
			pres.append(float(p)/10.0)
			altt.append(float(a))
			orin.append(float(o))
			acel.append(float(g)-9.78)
			time.append(int(m))
	file.close()

	altt = list(map(lambda x:x-(min(altt)), altt))

	plt.style.use('seaborn')
	fig = plt.figure(1)
	fig.suptitle('CanSat')

	if g == 't':
		g_temp(fig,time, temp)
	elif g == 'p':
		g_pres(fig,time, pres)
	elif g == 'a':
		g_alt(fig,time, altt)
	elif g == 'c':
		g_acel(fig,time, acel)
	else:
		at = fig.add_subplot(111)
		at.plot(time, temp, 'r-', label='Temperatura (0C)')
		at.plot(time, altt, 'm-', label='Altura (m)')
		at.plot(time, pres, 'c-', label='Presion (kPa)')
		at.plot(time, acel, 'g-', label='Aceleracion (m/s^2)')
		at.legend()
		plt.show()

def g_temp(fig, time, temp):
	at = fig.add_subplot(111)
	at.plot(time, temp, 'r-', label='Temperatura (0C)')
	at.legend()
	plt.show()

def g_pres(fig, time, pres):
	at = fig.add_subplot(111)
	at.plot(time, pres, 'c-', label='Presion (kPa)')
	at.legend()
	plt.show()

def g_alt(fig, time, altt):
	at = fig.add_subplot(111)
	at.plot(time, altt, 'm-', label='Altura (m)')
	at.legend()
	plt.show()

def g_acel(fig, time, acel):
	at = fig.add_subplot(111)
	at.plot(time, acel, 'g-', label='Aceleracion (m/s^2)')
	at.legend()
	plt.show()
