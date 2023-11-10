import pulp
from itertools import combinations
from matrix import *

# Formulación DFJ

# Crear un problema de minimización
problemaGG = pulp.LpProblem("CMA_DFJ", pulp.LpMinimize)

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
g = pulp.LpVariable.dicts("g", A, 0, n, pulp.LpInteger )

problemaGG += pulp.lpSum(C[i][j] * x[(i, j)] for (i, j) in A)

# Restricciones
for i in V:
    problemaGG += pulp.lpSum(x[(i, j)] for j in V if i != j) == 1

for j in V:
    problemaGG += pulp.lpSum(x[(i, j)] for i in V if i != j) == 1

for i in V[1:]:
    problemaGG += pulp.lpSum(g[(i, j)] for j in V if i != j) - pulp.lpSum(g[(j, i)] for j in V if i != j) == 1

for i in V:
    for j in V:
        if i != j:
            problemaGG += g[(i, j)] >= 0
            problemaGG += g[(i, j)] <= (n - 1) * x[(i, j)]


# Resolver el problema
problemaGG.solve()

# Imprimir la solución
print("Estado:", pulp.LpStatus[problemaGG.status])
for (i, j) in A:
    if x[(i, j)].varValue == 1:
        print(f"x({i},{j}) = 1")
print("Valor óptimo =", pulp.value(problemaGG.objective))