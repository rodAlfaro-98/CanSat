
def GText(name):

	import matplotlib.pyplot as plt

	temp = []
	pres = []
	altt = []
	orin = []
	acel = []
	time = []

	file = open(name, 'r')
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

	allt = list(map(lambda x:x-(min(altt)), altt))

	plt.style.use('seaborn')
	fig = plt.figure(1)
	fig.suptitle('CanSat')

	at = fig.add_subplot(111)
	at.plot(time, temp, 'r-', label='Temperatura (C)')
	at.plot(time, allt, 'm-', label='Altura (m)')
	at.plot(time, pres, 'c-', label='Presion (kPa)')
	at.plot(time, acel, 'g-', label='Aceleracion (m/s^2)')
	at.legend()

	plt.show()
