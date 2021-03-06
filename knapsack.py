#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import matplotlib.pyplot as plt
import gc

# vec_w es el vector de pesos de cada uno de los elementos
# vec_w es el vector de valores de cada uno de los elementos
vec_w = []
vec_v = []

# optVal es la solución óptima de la instancia según Pisinger
# vec_selec es vector de 1s y 0s según si se elige o no ese elem. en
# la solución óptima según Pisinger
optVal = 0
vec_selec = []

# seleccionados es el vector de 1s y 0s según si se elige o no ese elem.
# según nuestro algoritmo resuelve mochila
seleccionados = []
# Vector de soluciones parciales mochila(j, w)
soluciones = []

def parsear_instancia(f):	
	f.readline() # Leo el título de la instancia
	cantElem =  int(f.readline().split()[1]) # Leo C
	capMochila = int(f.readline().split()[1]) # Leo W
	valOpt = int(f.readline().split()[1]) # Leo la sol. optima
	f.readline() # Leo el tiempo que tardo la instancia
	i = 0
	while (i < cantElem):
		lineAct = f.readline().split(',')
		vec_v.append(int(lineAct[1]))
		vec_w.append(int(lineAct[2]))
		vec_selec.append(int(lineAct[3]))

		i += 1
	f.readline() # Leo línea de separación --------
	f.readline() # Leo la línea en blanco
	
	return (cantElem, capMochila, valOpt)

def mochilaReal(i, w):
	if(i < 0):
		return 0
	if w < vec_w[i]:
		if soluciones[i-1].has_key(w):
			return soluciones[i-1][w]
		else:
			return mochilaReal(i-1, w)
	else:
		if soluciones[i-1].has_key(w):
			noIncluir = soluciones[i-1][w]
		else:
			noIncluir = mochilaReal(i-1, w)
		if soluciones[i-1].has_key(w - vec_w[i]):
			siIncluir = soluciones[i-1][w - vec_w[i]] + vec_v[i]
		else:
			siIncluir = mochilaReal(i-1, w - vec_w[i]) + vec_v[i]
	soluciones[i][w] = max(noIncluir, siIncluir)
	return soluciones[i][w]
	
	
def mochilaEntera(cantElem, capMochila):
	for w in range (0, capMochila+1):
		soluciones[0][w] = 0
	for i in range (0, cantElem+1):
		soluciones[i][0] = 0
	for i in range (1, cantElem+1):
		for w in range (0, capMochila+1):
			if (vec_w[i-1] <= w):
				soluciones[i][w] = max(soluciones[i-1][w] ,soluciones[i-1][w - vec_w[i-1]] + vec_v[i-1])
			else:
				soluciones[i][w] = soluciones[i-1][w]
	return soluciones[cantElem][capMochila]

def seleccionar_elementos(C, w):
	for i in range (C, -1, -1):
		if (mochilaReal(i, w) != mochilaReal(i-1, w)):
			seleccionados[i] = 1
			w -= vec_w[i]


# De acá en adelante es la zona de tests

llamarEntera = True

arch = "Mochila/Dificiles/"
arch += "knapPI_12_500_1000.csv"
f = open(arch, 'r')
dist_tiempos = []
tProm = 0.0
for instanciaAct in range (0, 100):
	vec_w = []
	vec_v = []
	cantElem = 0
	Wmochila = 0
	optVal = 0
	vec_selec = []
	seleccionados = []
	soluciones = []

	gc.collect()

	(cantElem, Wmochila, optVal) = parsear_instancia(f)
	if(llamarEntera):
		solve_mochila = mochilaEntera
		cantElem += 1
		for i in range(0, cantElem):
			dic = []
			soluciones.append(dic)
			for w in range (0, Wmochila+1):
				soluciones[i].append(0)
	else:
		solve_mochila = mochilaReal
		for i in range(0, cantElem):
			dic = {}
			soluciones.append(dic)

	for i in range (0, cantElem):
		seleccionados.append(0)
	print "Instancia actual: ", instanciaAct + 1
	
	t0 = time.time()
	a = solve_mochila(cantElem-1, Wmochila)
	t1 = time.time()

	print "Sol. óptima encontrada: ", a == optVal
	print a
	deltaT = t1 - t0
	tProm += (deltaT * 0.01)
	print "Tiempo: ", deltaT 
	dist_tiempos.append(deltaT)
f.close()

print "Tiempo promedio: ", tProm

plt.hist(dist_tiempos, bins=15, histtype='stepfilled', color='b', stacked=True, alpha = 1.0, label="knapPI_13_50_1000")
plt.title("Dist. de tiempos")
plt.xlabel("Tiempo [seg.]")
plt.ylabel("Frecuencia")
plt.grid(True)
#plt.ylim(0, 9)
#plt.legend()
plt.show()

#	seleccionar_elementos(cantElem-1, Wmochila)
#	print "Combinación óptima encontrada: ", seleccionados == vec_selec

