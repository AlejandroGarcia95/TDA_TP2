class Arista(object):
	''' Clase Arista. Se crea con un nodo fuente u, un nodo sumidero v y la capacidad 
	de la arista w. RevArista es la arista que va de v hacia u. '''
	def __init__(self,u,v,w):
		self.fuente = u
		self.sumidero = v
		self.capacidad = w
		self.revArista = None
		
	def __str__(self):
		return "%s -> %s: %s" %(self.fuente, self.sumidero, self.capacidad)


class RedDeFlujo(object):
	''' Clase RedDeFlujo. Se crea un diccionario con los adyacentes a un vertice y otro con 
    el flujo correspondiente a cada arista. Se calcula el flujo maximo utilizando el algoritmo 
    de Ford-Fulkerson. El metodo obtenerCamino es el que busca un augmenting path de s a t 
    mediante DFS.'''
	def __init__(self):
		self.adyacentes = {}
		self.flujo = {}
		
	def agregarVertice(self, vertice):
		self.adyacentes[vertice] = []
		
	def obtenerAristas(self, vertice):
		return self.adyacentes[vertice]
		
	def agregarArista(self, u, v, w = 0):
		arista = Arista(u,v,w)
		revArista = Arista(v,u,0)
		arista.revArista = revArista
		revArista.revArista = arista
		self.adyacentes[u].append(arista)
		self.adyacentes[v].append(revArista)
		self.flujo[arista] = 0
		self.flujo[revArista] = 0
		
	def obtenerCamino(self, s, t, camino):
		if s == t:
			return camino 
		for arista in self.obtenerAristas(s):
			residual = arista.capacidad - self.flujo[arista]
			if residual > 0 and arista not in camino:
				final = self.obtenerCamino(arista.sumidero, t, camino + [arista])
				if final != None:
					return final
				
				
	def flujoMaximo(self,s,t):
		residuales = []
		flujoMax = 0
		camino = self.obtenerCamino(s,t,[])
		while camino != None:
			for arista in camino:
				residuales.append(arista.capacidad - self.flujo[arista])
			flujo = min(residuales)
			for arista in camino:
				self.flujo[arista] += flujo
				self.flujo[arista.revArista] -= flujo
			camino = self.obtenerCamino(s,t,[])
	
		for arista in self.obtenerAristas(s):
			flujoMax += self.flujo[arista]
			
		return flujoMax

''' Crea un flujo de red a partir de un archivo con el formato especificado en el enunciado.
Si cormen es True, la red obtenida seguira las relaciones propuestas por el libro Cormen 
mientras que si es False, seguira las que propone Kleinberg & Tardos. '''
def crearRed(archivo, cormen = False):
	arch = open(archivo,"r")
	
	cantAreas = int(arch.readline())
	cantProyectos = int(arch.readline())
	
	red = RedDeFlujo()
	red.agregarVertice("s")
	red.agregarVertice("t")
	for area in range(cantAreas):
		ar = "A" + str(1 + area)
		red.agregarVertice(ar)
		if cormen:
			red.agregarArista("s", ar, int(arch.readline()))
		else:
			red.agregarArista(ar, "t", int(arch.readline()))
		
	for proyecto in range(cantProyectos):
		pr = "P" + str(1 + proyecto)
		red.agregarVertice(pr)
		linea = arch.readline().split()
		if cormen:
			red.agregarArista(pr, "t", int(linea[0]))
		else:
			red.agregarArista("s", pr, int(linea[0]))
		linea = linea[1:]
		for dato in linea:
			if cormen:
				red.agregarArista("A" + str(dato), pr, float("inf"))
			else:
				red.agregarArista(pr, "A" + str(dato), float("inf"))
			
	arch.close()
	if cormen:
		return (red,cantProyectos)
	return red

''' Realiza una busqueda en profundidad a partir del grafo residual, el nodo inicial s y 
una lista con los nodos que se van visitando. Finalmente, visitados sera el conjunto S 
de todos los nodos alcanzables por s, que constituyen la solucion al problema.'''
def dfs(grafoRes, inicial, visitados):
	visitados.append(inicial)
	for siguiente in grafoRes.obtenerAristas(inicial):
		if (siguiente.capacidad - grafoRes.flujo[siguiente]) > 0 and siguiente.sumidero not in visitados:
			dfs(grafoRes, siguiente.sumidero, visitados)

''' Obtiene las aristas que cruzan el corte minimo entre s y t. '''		
def obtenerAristasCorteMin(red):
	visitados = []
	aristasCorteMin = []
	dfs(red, "s", visitados)
	
	for elemento in visitados:
		if elemento[0] == "A":
			continue
		for arista in (red.obtenerAristas(elemento)):
			if not arista.capacidad:
				continue
			if (arista.sumidero not in visitados):
				aristasCorteMin.append(arista)
				
	return aristasCorteMin

''' A partir del flujo de red y de las aristas de corte minimo, obtiene los 
expertos a contratar para la version del Cormen.'''
def expertosContratados(red, aristasCorteMin):
	expertos = ""
	for adyacente in red.obtenerAristas("s"):
		if adyacente in aristasCorteMin:
			expertos += "E" + adyacente.sumidero[1:] + " "
			
	return expertos
	
	
''' A partir del flujo de red, de las aristas de corte minimo y de la cantidad de 
proyectos posibles, obtiene los proyectos a aceptar para la version del Cormen.'''	
def proyectosAceptados(red, aristasCorteMin, cantProy):
	proyectos = ""
	for proy in range(cantProy):
		if red.obtenerAristas("P" + str(proy + 1))[0] not in aristasCorteMin:
			proyectos += "P" + str(proy + 1) + " "
			
	return proyectos

''' Algoritmo que resuelve el problema de seleccion de proyectos a partir de un 
archivo con el formato pedido. Devuelve los proyectos y expertos seleccionados. '''
def determinarProyectosExpertos(archivo):
	visitados = []
	red = crearRed(archivo)
	red.flujoMaximo("s","t")
	dfs(red, "s", visitados)
	
	visitados.remove("s")
	p = "Proyectos a aceptar: "
	e = "Expertos a contratar: "
	
	for elemento in visitados:
		if elemento[0] == "P":
			p += elemento + " "
		else:
			e += "E" + elemento[1:] + " "
			
	return p + ", " + e
	
''' Algoritmo que resuelve el problema de seleccion de proyectos a partir de un 
archivo con el formato pedido. Lo resuelve siguiendo lo propuesto por el Cormen.
Devuelve los proyectos y expertos seleccionados. '''
def determinarProyectosExpertosCormen(archivo):
	visitados = []
	datos = crearRed(archivo, True)
	red = datos[0]
	red.flujoMaximo("s","t")
	dfs(red, "s", visitados)
	arMin = obtenerAristasCorteMin(red)
	exp = expertosContratados(red,arMin)
	proy = proyectosAceptados(red, arMin, datos[1])
			
	return "Proyectos a aceptar: " + proy + ", Expertos a contratar: " + exp



'''Seccion de pruebas'''
	
# Prueba Ford-Fulkerson	
'''
g = RedDeFlujo()
[g.agregarVertice(v) for v in "sopqrt"]
g.agregarArista("s","o",3)
g.agregarArista("s","p",3)
g.agregarArista("o","p",2)
g.agregarArista("o","q",3)
g.agregarArista("p","r",2)
g.agregarArista("r","t",3)
g.agregarArista("q","r",4)
g.agregarArista("q","t",2)
print (g.flujoMaximo("s","t")) == 5
'''

# Prueba con el archivo y los dos tipos de redes
'''
datos = crearRed("ejemplotp.txt", True)
red = datos[0] 
print red.flujoMaximo("s","t")
ar = obtenerAristasCorteMin(red)
print expertosContratados(red,ar)
print proyectosAceptados(red, ar, datos[1])


red = crearRed("ejemplotp.txt")
red.flujoMaximo("s","t")
visitados = []
dfs(red, "s", visitados)
print visitados
'''

# Prueba expertos y proyectos I
'''
red = RedDeFlujo()
red.agregarVertice("s")
red.agregarVertice("t")
red.agregarVertice("P1")
red.agregarVertice("P2")
red.agregarVertice("P3")
red.agregarVertice("A1")
red.agregarVertice("A2")
red.agregarVertice("A3")

red.agregarArista("s","A1",200)
red.agregarArista("s","A2",100)
red.agregarArista("s","A3",50)
red.agregarArista("P1","t",100)
red.agregarArista("P2","t",200)
red.agregarArista("P3","t",150)
red.agregarArista("A1","P1",float("inf"))
red.agregarArista("A2","P1",float("inf"))
red.agregarArista("A2","P2",float("inf"))
red.agregarArista("A3","P3",float("inf"))
red.flujoMaximo("s","t")
ar = obtenerAristasCorteMin(red)
print expertosContratados(red,ar)
print proyectosAceptados(red, ar, 3)
'''

# Prueba aristas corte minimo
'''
g = RedDeFlujo()
[g.agregarVertice(v) for v in "s1234t"]
g.agregarArista("s","1",16)
g.agregarArista("s","2",13)
g.agregarArista("1","3",12)
g.agregarArista("1","2",10)
g.agregarArista("2","1",4)
g.agregarArista("2","4",14)
g.agregarArista("3","2",9)
g.agregarArista("3","t",20)
g.agregarArista("4","3",7)
g.agregarArista("4","t",4)
g.flujoMaximo("s","t")
arMin = obtenerAristasCorteMin(g)
for arista in arMin:
	print arista
'''

# Prueba expertos y proyectos II
'''
red = RedDeFlujo()
red.agregarVertice("s")
red.agregarVertice("t")
red.agregarVertice("P1")
red.agregarVertice("P2")
red.agregarVertice("P3")
red.agregarVertice("A1")
red.agregarVertice("A2")
red.agregarVertice("A3")

red.agregarArista("s","P1",100)
red.agregarArista("s","P2",200)
red.agregarArista("s","P3",150)
red.agregarArista("A1","t",200)
red.agregarArista("A2","t",100)
red.agregarArista("A3","t",50)
red.agregarArista("P1","A1",float("inf"))
red.agregarArista("P1","A2",float("inf"))
red.agregarArista("P2","A2",float("inf"))
red.agregarArista("P3","A3",float("inf"))
red.flujoMaximo("s","t")
visitados = []
dfs(red, "s", visitados)
print visitados
'''

## Prueba algoritmo final

## Pruebas generales
#print determinarProyectosExpertos("ejemplotp.txt")
#print determinarProyectosExpertosCormen("ejemplotp.txt")
#print determinarProyectosExpertos("t1.txt")
#print determinarProyectosExpertosCormen("t1.txt")
#print determinarProyectosExpertos("t5.txt")
#print determinarProyectosExpertosCormen("t5.txt")
#print determinarProyectosExpertos("t6.txt")
#print determinarProyectosExpertosCormen("t6.txt")
#print determinarProyectosExpertos("t7.txt")
#print determinarProyectosExpertosCormen("t7.txt")
#print determinarProyectosExpertos("t8.txt")
#print determinarProyectosExpertosCormen("t8.txt")
#print determinarProyectosExpertos("t9.txt")
#print determinarProyectosExpertosCormen("t9.txt")
#print determinarProyectosExpertos("t10.txt")
#print determinarProyectosExpertosCormen("t10.txt")
#print determinarProyectosExpertos("t11.txt")
#print determinarProyectosExpertosCormen("t11.txt")

## Prueba ganancia igual a costo
#print determinarProyectosExpertos("t2.txt")
#print determinarProyectosExpertosCormen("t2.txt")

## Prueba "conviene todo"
#print determinarProyectosExpertos("t3.txt")
#print determinarProyectosExpertosCormen("t3.txt")

## Prueba "no conviene nada"
#print determinarProyectosExpertos("t4.txt")
#print determinarProyectosExpertosCormen("t4.txt")
