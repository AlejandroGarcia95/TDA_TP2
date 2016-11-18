#coding=utf-8
import time
import gc

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
	for i in range(0, len(s)):
		m = s[i]
		dist = d[(s, m)]
		dist = (dist[0] + adj[m][k], dist[1] + (m,))
		# Si no vi ningún mínimo, o si encontré un resultado mejor
		if ( (dist[0] < minimo[0]) or (minimo[1] == 0) ):
			minimo = dist
	return minimo


def solve(adj, n):
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
	subsets = []
	for i in range(1, n):
		s = (i,)
		d[(s,i)] = (adj[0][i], (0,))
		subsets.append(s)
	
	# Para cada longitud de camino posible
	for m in range(2, n):
		dnew = {}
		loop_start = time.time()
		# Obtengo los subsets de |s| = m
		
		new_subsets = []
		for elem in subsets:
			for i in range(elem[-1] + 1, n):
				new_subsets.append(elem + (i,))
		subsets = new_subsets
		
		loop_set = time.time()
		# Para cada subset de m vértices
		for s in subsets:
			# Para cada vértice en el subset
			for i in range(0, len(s)):
				k = s[i]
				tmp = s[0:i] + s[i+1:len(s)]
				dnew[(s, k)] = computar_minimo(d, tmp, k, adj)
		
		loop_end = time.time()
		#print "Iteracion: ", m, " armando subconj ", loop_set-loop_start, " computando minimo ", loop_end-loop_set, " total ", loop_end-loop_start
		d = dnew
		dnew = {}
		gc.collect()
	
	# Ya tengo todos los caminos mínimos que pasan por todos los nodos
	# Falta ver cual es el que genera distancia menor de vuelta al origen
	minimo = (0, 0)
	s = tuple([i for i in range(1, n)])
	for k in s:
		dist = d[(s, k)]
		dist = (dist[0] + adj[k][0], dist[1] + (k,))
		if ( (dist[0] < minimo[0]) or (minimo[1] == 0) ):
			minimo = dist
	
	return minimo
