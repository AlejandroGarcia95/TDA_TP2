class Arista(object):
	def __init__(self,u,v,w):
		self.fuente = u
		self.sumidero = v
		self.capacidad = w
		self.revArista = None
		
	def __str__(self):
		return "%s -> %s: %s" %(self.fuente, self.sumidero, self.capacidad)
		
class RedDeFlujo(object):
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

def crearRed(archivo):
	arch = open(archivo,"r")
	
	cantAreas = int(arch.readline())
	cantProyectos = int(arch.readline())
	
	red = RedDeFlujo()
	red.agregarVertice("s")
	red.agregarVertice("t")
	for area in range(cantAreas):
		ar = "A" + str(1 + area)
		red.agregarVertice(ar)
		red.agregarArista("s", ar, int(arch.readline()))
		
	for proyecto in range(cantProyectos):
		pr = "P" + str(1 + proyecto)
		red.agregarVertice(pr)
		linea = arch.readline().split()
		red.agregarArista(pr, "t", int(linea[0]))
		linea = linea[1:]
		for dato in linea:
			red.agregarArista("A" + str(dato), pr, float("inf"))
			
	arch.close()
	return red

def dfs(red, inicial, visitados):
	visitados.append(inicial)
	for siguiente in red.obtenerAristas(inicial):
		if (siguiente.capacidad - red.flujo[siguiente]) > 0 and siguiente.sumidero not in visitados:
			dfs(red, siguiente.sumidero, visitados)
		
def obtenerAristasCorteMin(red):
	visitados = []
	aristasCorteMin = []
	dfs(red, "s", visitados)
	
	for elemento in visitados:
		for arista in (red.obtenerAristas(elemento)):
			if not arista.capacidad:
				continue
			if (arista.sumidero not in visitados):
				aristasCorteMin.append(arista)
				
	return aristasCorteMin

def expertosContratados(red,aristasCorteMin):
	expertos = []
	for adyacente in red.obtenerAristas("s"):
		if adyacente in aristasCorteMin:
			expertos.append(adyacente.sumidero[1:])
			
	return expertos
			
def proyectosAceptados(red, aristasCorteMin, cantProy):
	proyectos = []
	for proy in range(cantProy):
		if red.obtenerAristas("P" + str(proy + 1))[0] not in aristasCorteMin:
			proyectos.append("P" + str(proy + 1))
			
	return proyectos
	
	
''' Ej wiki		
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
print (g.flujoMaximo("s","t"))

'''
'''
red = crearRed("ejemplotp.txt")
red.flujoMaximo("s","t")
ar = obtenerAristasCorteMin(red)
print expertosContratados(red,ar)
print proyectosAceptados(red, ar, 2)
'''

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
