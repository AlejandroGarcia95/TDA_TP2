#coding=utf-8
import random
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
	subsets = []
	for i in range(1, n):
		s = (i,)
		d[(s,i)] = (adj[0][i], 0)
		subsets.append(s)
	
	# Para cada longitud de camino posible
	for m in range(2, n):
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
				d[(s, k)] = computar_minimo(d, tmp, k, adj)
		
		loop_end = time.time()
		gc.collect()
		print "Iteracion: ", m, " armando subconj ", loop_set-loop_start, " computando minimo ", loop_end-loop_set, " total ", loop_end-loop_start
	
	
	# Ya tengo todos los caminos mínimos que pasan por todos los nodos
	# Falta ver cual es el que genera distancia menor de vuelta al origen
	minimo = (0, 0)
	s = tuple([i for i in range(1, n)])
	for k in s:
		dist = d[(s, k)]
		dist = (dist[0] + adj[k][0], k)
		if ( (dist[0] < minimo[0]) or (minimo[1] == 0) ):
			minimo = dist
	
	# Reconstruyo el camino
	camino = [0]
	last = minimo[1]
	for i in range(1, n):
		camino = [last] + camino
		dist = d[(s, last)]
		for j in range(0, len(s)):
			if (s[j] == last):
				tmp = s[0:j] + s[j+1:len(s)]
		s = tmp
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


#for i in range(4, 48):
#	adj = mat_rnd(i)
#	print "\nCamino mínimo: ", i
#	start = time.time()
#	print tsp_dinamico(adj, i)
#	end = time.time()
#	print(end-start)
#	gc.collect()


# Cargar de archivo. IMPORTANTE: una línea = una fila, no agregar lineas en blanco al final
file = open("test2.txt")
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

		
		
