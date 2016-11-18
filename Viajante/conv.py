#coding=utf-8
import math

def from_simetric(path_in, path_out, n):
	in_file = open(path_in)
	half = []
	for line in in_file:
		for e in line.split():
			half.append(float(e))
			
	out_file = open(path_out, 'w')
	ady = []
	for i in range(0, n):
		ady.append([x for x in range(0,n)])
	count = 0
	for i in range(0,n):
		for j in range(0, i+1):
			ady[i][j] = half[count]
			ady[j][i] = half[count]
			count += 1
	for r in ady:
		for e in r:
			out_file.write(str(e) + "\t")
		out_file.write("\n")
	out_file.close()
	in_file.close()

def from_vertex(vertices, path):
	u"""Crea una matriz de ady a partir de una lista de nodos"""
	out_file = open(path, 'w')
	for v in vertices:
		for w in vertices:
			if (v == w):
				out_file.write("0 ")
			else:
				aux = (v[0] - w[0], v[1] - w[1])
				dist = math.sqrt(aux[0]*aux[0] + aux[1]*aux[1])
				out_file.write(str(dist) + " ")
		out_file.write("\n")
	out_file.close()

def read_vertex(path):
	in_file = open(path)
	vertices = []
	for line in in_file:
		v = []
		for elem in line.split():
			v.append(float(elem))
		vertices.append(v)
	in_file.close()
	print vertices
	return vertices


def convert_to_dl(s, d, n):
	in_file = open(s)
	out_file = open(d, 'w')
	out_file.write("dl\n")
	out_file.write("format = edgelist1\n")
	out_file.write("n = " + str(n) + "\n")
	out_file.write("labels embedded:\n")
	out_file.write("data:\n")
	
	i = 0
	for line in in_file:
		j = 0
		for number in line.split():
			if (not (i == j)):
				out_file.write(str(i) + " " + str(j) + " " + str(float(number)) + "\n")
			j = j+1
		i = i+1
	
	in_file.close()
	out_file.close()


vertices = [(0, 0), (1, 0), (1, 1), (0, 2)]
path_out = "fri26.out"
path_in = "fri26.in"

#from_vertex(read_vertex(path_in), path_out)
from_simetric(path_in, path_out, 26)
