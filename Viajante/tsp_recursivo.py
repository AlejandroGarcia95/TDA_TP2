#coding=utf-8

def tsp_recursivo(s, v, ady, d):
	if (len(s) == 1):
		elem = next(iter(s))
		return (ady[0][elem], (0,))
	
	tmp = set(s)
	tmp.remove(v)
	tmp = frozenset(tmp)
	minimo = (0, 0)
	for w in tmp:
		key = (tmp, w)
		if (key not in d):
			d[key] = tsp_recursivo(tmp, w, ady, d)
		value = (d[key][0] + ady[w][v], w) #d[key][1] + (w,))
		if (minimo[0] > value[0] or minimo[1] == 0):
			minimo = value
	return minimo


def solve(ady, n):
	d = {}
	s = set([x for x in range(0,n)])
	minimo = tsp_recursivo(s, 0, ady, d)
	
	# return minimo
	
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
