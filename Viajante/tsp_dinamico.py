#coding=utf-8
import random
import time
import gc

def subsets(m, n, idx, prev):
	u"""Devuelve un set con todas los subsets de {idx..n}, de tamaño m.
	
	Parámetros:
	m -- tamaño de los subsets a formar.
	n -- tamaño del set original.
	idx -- elemento inicial del set original.
	
	Los subsets se forman sin incluir permutaciones.
		i.e. {2, 3, 4} = {3, 2, 4}
	El set original de tamaño n se forma con los enteros de 0 hasta n-1.
	Los subsets a formar no incluyen los primeros idx elementos.
	
	Devuelve un set de todos los subsets s tq:
		|s| = m
		s contenido en N = {idx, idx+1, idx+2, ... , n-2, n-1}
	"""
	
	# Casos base
	if (m == 1):
		return [[i] for i in range(idx, n)]
	
	if (idx > n-m):
		return []
	
	sets = []
	if ((m-1, n, idx+1) in prev):
		sset = prev[(m-1, n, idx+1)]
	else:
		prev[(m-1, n, idx+1)] = subsets(m-1, n, idx+1, prev)
		sset = prev[(m-1, n, idx+1)]
	
	for s in sset:
		sets += [[idx] + s]
		
	if ((m, n, idx+1) in prev):
		sset = prev[(m, n, idx+1)]
	else:
		prev[(m, n, idx+1)] = subsets(m, n, idx+1, prev)
		sset = prev[(m, n, idx+1)]
	sets += sset
	return sets


def computar_minimo(d, s, k, adj):
	u"""Computa el camino minimo que pasa por todos los nodos de s y termina en k.
	
	Parámetros:
	d -- Diccionario que contiene los caminos minimos de long |act|-1.
	s -- Conjunto de vétitces por los que pasa el camino.
	k -- Vértice perteneciente a s donde debe terminar el camino.
	adj -- Matriz de adyacencia del grafo.
	
	Devuelve:
	Una tupla (d, p).
	Donde d = min[ dist[(s-m, k)] + adj[m][k] ] para todo m != k en s
	Y p = m tq d sea mínimo.
	Obs: dist[(s, k)] = d[(s, k)][0]
	"""
	
	minimo = (0, 0)
	
	tmp = set(s)
	tmp.remove(k)
	tmp = frozenset(tmp)
	for m in s:
		if (m != k):
			dist = d[(tmp, m)]
			dist = (dist[0] + adj[m][k], m)
			# Si no vi ningún mínimo, o si encontré un resultado mejor
			if ( (dist[0] < minimo[0]) or (minimo[1] == 0) ):
				minimo = dist
	return minimo


def tsp_dinamico(adj, n):
	u"""Resuelve el problema del viajante asimétrico con n nodos.
	
	Parámetros:
	adj -- la matriz de adyacencia del grafo (nxn).
	n -- la cantidad de nodos del grafo.
	"""
	
	# Diccionario que almacenará los resultados parciales del algoritmo
	# de programación dinámica.
	# key:value = (S, k):(d, p)
	# (S, k) representa al camino mínimo que pasa por todos los nodos de
	# S y termina en k, que tiene un peso d y p como el nodo anterior a 
	# k, para reconstruir el camino.
	d = {}
	
	# Inicializo la estructura de la tabla de soluciones parciales
	for i in range(1, n):
		s = frozenset([i])
		d[(s,i)] = (adj[0][i], 0)
	
	# Para cada longitud de camino posible
	for m in range(2, n):
		
		loop_start = time.time()
		# Para cada subset de m vértices
		ssets = subsets(m, n, 1, {})
		loop_set = time.time()
		for s in ssets:
			# Para cada vértice en el subset
			fss = frozenset(s)
			for k in s:
				d[(fss, k)] = computar_minimo(d, s, k, adj)
		
		loop_end = time.time()
		gc.collect()
		print "Iteracion: ", m, " armando subconj ", loop_set-loop_start, " computando minimo ", loop_end-loop_set, " total ", loop_end-loop_start
	
	
	# Ya tengo todos los caminos mínimos que pasan por todos los nodos
	# Falta ver cual es el que genera distancia menor de vuelta al origen
	minimo = (0, 0)
	s = set([i for i in range(1, n)])
	fss = frozenset(s)
	for k in s:
		dist = d[(fss, k)]
		dist = (dist[0] + adj[k][0], k)
		if ( (dist[0] < minimo[0]) or (minimo[1] == 0) ):
			minimo = dist
	
	# Reconstruyo el camino
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
		

# Matriz random, asimétrica
i = 20
ady = mat_rnd(i)

start = time.time()
print tsp_dinamico(ady, i)
end = time.time()

		
