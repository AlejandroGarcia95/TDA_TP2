#coding=utf-8
import random
import time
import gc
import tsp_dinamico as tsp_d
import tsp_recursivo as tsp_r

def mat_rnd(n):
	u"""Genera una matriz aleatoria de nxn"""
	
	mat = []
	for i in range(0, n):
		tmp = []
		for j in range(0, n):
			tmp.append(random.randint(1, 50))
		mat.append(tmp)
	return mat

def load_ady(path):
	u"""Lee la matriz de adyacencia de un archvio y devuelve una tupla con la matriz y el tamaño de la misma"""
	file = open(path)
	ady = []
	i = 0
	for line in file:
		tmp = []
		for number in line.split():
			tmp.append(float(number))
		ady.append(tmp)
		i += 1
	return ady


def test_file(path, iteraciones):
	ady = load_ady(path)
	n = len(ady)
	
	print "PRUEBA DE: ", path, " CON ", iteraciones, " ITERACIONES"
	
	if (n <= 21):
		print "\nMETODO RECURSIVO:"
		acum = 0.0
		for i in range(0, iteraciones):
			start = time.time()
			sol = tsp_r.solve(ady, n)
			end = time.time()
			acum += end-start
			gc.collect()
		print "SOLUCION: ", sol
		print "TIEMPO ACUMULADO: ", acum
		print "TIEMPO PROMEDIO: ", (float(acum)/iteraciones)
	
	print "\nMETODO ITERATIVO:"
	acum = 0.0
	for i in range(0, iteraciones):
		start = time.time()
		sol = tsp_d.solve(ady, n)
		end = time.time()
		acum += end-start
		gc.collect()
	print "SOLUCION: ", sol
	print "TIEMPO ACUMULADO: ", acum
	print "TIEMPO PROMEDIO: ", (float(acum)/iteraciones)
	print "\n"


def test_random(n, iteraciones):
	ady = mat_rnd(n)

	print "PRUEBA RANDOM CON ", n, " NODOS, USANDO ", iteraciones, " ITERACIONES"
	
	if (n <= 21):
		print "\nMETODO RECURSIVO:"
		acum = 0.0
		for i in range(0, iteraciones):
			start = time.time()
			sol = tsp_r.solve(ady, n)
			end = time.time()
			acum += end-start
			gc.collect()
		print "SOLUCION: ", sol
		print "TIEMPO ACUMULADO: ", acum
		print "TIEMPO PROMEDIO: ", (float(acum)/iteraciones)

	print "\nMETODO ITERATIVO:"
	acum = 0.0
	for i in range(0, iteraciones):
		start = time.time()
		sol = tsp_d.solve(ady, n)
		end = time.time()
		acum += end-start
		gc.collect()
	print "SOLUCION: ", sol
	print "TIEMPO ACUMULADO: ", acum
	print "TIEMPO PROMEDIO: ", (float(acum)/iteraciones)
	print "\n"
	
tests = ["tests/p01.tsp", "tests/gr17.tsp", "tests/ulysses16.tsp", "tests/gr21.tsp", "tests/ulysses22.tsp"]

for elem in tests:
	test_file(elem, 10)
	gc.collect()
for i in range(5, 22):
	test_random(i, 10)
	gc.collect()

