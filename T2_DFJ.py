import pulp
from itertools import combinations
from matrix import *

# Formulación DFJ

# Crear un problema de minimización
problemaDFJ = pulp.LpProblem("CMA_DFJ", pulp.LpMinimize)

# Leer la matriz de costos desde un archivo
with open('m14a.txt', 'r') as f:
    matrix = [[int(num) for num in line.split()] for line in f]

#Matriz de costos
C = matrix

# Conjuntos de nodos y aristas
n=len(C) # Tamaño del problema
V = range(n)  # Vertices
A = [(i, j) for i in V for j in V if i != j] # Aristas

# Variables binarias x_ij
x = pulp.LpVariable.dicts("x", A, 0, 1, pulp.LpBinary)
#c = pulp.LpVariable.dicts("c", V, 0, n, pulp.LpInteger )

problemaDFJ += pulp.lpSum(C[i][j] * x[(i, j)] for (i, j) in A)

# Restricciones
for i in V:
    problemaDFJ += pulp.lpSum(x[(i, j)] for j in V if i != j) == 1

for j in V:
    problemaDFJ += pulp.lpSum(x[(i, j)] for i in V if i != j) == 1


for s in range(2, n):
    for S in combinations(range(n), s):
        problemaDFJ += pulp.lpSum([x[i, j] for i in S for j in S if i != j]) <= len(S) - 1

# Resolver el problema
problemaDFJ.solve()

# Imprimir la solución
print("Estado:", pulp.LpStatus[problemaDFJ.status])
for (i, j) in A:
    if x[(i, j)].varValue == 1:
        print(f"x({i},{j}) = 1")
print("Valor óptimo =", pulp.value(problemaDFJ.objective))



