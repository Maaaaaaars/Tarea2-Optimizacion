import pulp
from itertools import combinations

# Formulación DFJ

# Crear un problema de minimización
problemaDFJ = pulp.LpProblem("CMA_DFJ", pulp.LpMinimize)

#Matriz de costos
C=[[0,12,29,22,13,24],[12,0,19,3,25,6],[29,19,0,21,23,28],[22,3,21,0,4,5],[13,25,23,4,0,16],[24,26,28,5,16]]

# Conjuntos de nodos y aristas
n=len(C) # Tamaño del problema
V = range(n)  # Vertices
A = [(i, j) for i in V for j in V if i != j] # Aristas

# Variables binarias x_ij
x = pulp.LpVariable.dicts("x", A, 0, 1, pulp.LpBinary)
c = pulp.LpVariable.dicts("c", V, 0, n, pulp.LpInteger )

problemaDFJ += pulp.lpSum(C[i][j] * x[(i, j)] for (i, j) in A)

# Restricciones
for i in V:
    problemaDFJ += pulp.lpSum(x[(i, j)] for j in V if i != j) == 1

for j in V:
    problemaDFJ += pulp.lpSum(x[(i, j)] for i in V if i != j) == 1

for r in range(2, n):
    for S in combinations(V, r):
        for i in S:
            problemaDFJ += pulp.lpSum(x[(i, j)] for j in S if i != j) <= len(S) - 1

# Resolver el problema
problemaDFJ.solve()

# Imprimir la solución
print("Estado:", pulp.LpStatus[problemaDFJ.status])
for (i, j) in A:
    if x[(i, j)].varValue == 1:
        print(f"x({i},{j}) = 1")
print("Valor óptimo =", pulp.value(problemaDFJ.objective))


