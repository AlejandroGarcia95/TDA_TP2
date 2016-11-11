#coding=utf-8
import time
import random

def tsp_recursivo(s, v, ady, d):
	if (len(s) == 1):
		elem = next(iter(s))
		return (ady[0][elem], 0)
	
	tmp = set(s)
	tmp.remove(v)
	tmp = frozenset(tmp)
	minimo = (0, 0)
	for w in tmp:
		key = (tmp, w)
		if (key not in d):
			d[key] = tsp_recursivo(tmp, w, ady, d)
		value = (d[key][0] + ady[w][v], w)
		if (minimo[0] > value[0] or minimo[1] == 0):
			minimo = value
	return minimo


def tsp_wrapper(ady, n):
	d = {}
	s = set([x for x in range(0,n)])
	minimo = tsp_recursivo(s, 0, ady, d)
	
	
	# Reconstruyo el camino
	s = set([x for x in range(1, n)])
	camino = [0]
	last = minimo[1]
	for i in range(1, n):
		camino = [last] + camino
		dist = d[(frozenset(s), last)]
		s.remove(last)
		last = dist[1]
	
	camino = [0] + camino
	return (camino, minimo[0])


def mat_rnd(n):
	mat = []
	for i in range(0, n):
		tmp = []
		for j in range(0, n):
			tmp.append(random.randint(1, 50))
		mat.append(tmp)
	return mat




file = open("test.txt")
ady = []
i = 0
for line in file:
	tmp = []
	for number in line.split():
		tmp.append(int(number))
	ady.append(tmp)
	i += 1
		
i = 5

# Matriz random, asimétrica
for i in range(15, 19):
	ady = mat_rnd(i)
	start = time.time()
	print i, " -- ", tsp_wrapper(ady, i)
	end = time.time()
	print end-start
