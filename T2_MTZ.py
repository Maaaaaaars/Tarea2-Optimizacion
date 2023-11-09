import pulp
from itertools import combinations
from matrix import *

# Formulación DFJ

# Crear un problema de minimización
problemaMTZ = pulp.LpProblem("CMA_DFJ", pulp.LpMinimize)

#Matriz de costos
matriz = Matrices()
C = matriz.m10a

# Conjuntos de nodos y aristas
n=len(C) # Tamaño del problema
V = range(n)  # Vertices
A = [(i, j) for i in V for j in V if i != j] # Aristas

# Variables binarias x_ij
x = pulp.LpVariable.dicts("x", A, 0, 1, pulp.LpBinary)
u = pulp.LpVariable.dicts("u", V, 0, n, pulp.LpInteger )

problemaMTZ += pulp.lpSum(C[i][j] * x[(i, j)] for (i, j) in A)

# Restricciones
for i in V:
    problemaMTZ += pulp.lpSum(x[(i, j)] for j in V if i != j) == 1

for j in V:
    problemaMTZ += pulp.lpSum(x[(i, j)] for i in V if i != j) == 1

for i in V:
    for j in V:
        if(i!=j and i>=1):
            problemaMTZ += u[i]-u[j]+1<=n*(1-x[(i,j)])

# Resolver el problema
problemaMTZ.solve()

# Imprimir la solución
print("Estado:", pulp.LpStatus[problemaMTZ.status])
for (i, j) in A:
    if x[(i, j)].varValue == 1:
        print(f"x({i},{j}) = 1")
print("Valor óptimo =", pulp.value(problemaMTZ.objective))