import pulp
from itertools import combinations

# Formulación DFJ

# Crear un problema de minimización
problemaMTZ = pulp.LpProblem("CMA_DFJ", pulp.LpMinimize)

#Matriz de costos
C=[[9999, 3, 5, 48, 48, 8, 8, 5, 5,3, 3, 0, 3, 5, 8, 8, 5],
   [3, 9999, 3, 48, 48, 8, 8, 5, 5, 0 ,0 ,3 ,0 ,3 ,8 ,8, 5],
   [5, 3, 9999, 72, 72, 48, 48, 24, 24, 3, 3, 5, 3, 0, 48, 48, 24],
   [48, 48, 74, 9999, 0, 6, 6, 12, 12, 48, 48, 48, 48, 74, 6, 6, 12],
   [48, 48, 74, 0, 9999, 6, 6, 12, 12, 48, 48, 48, 48, 74, 6, 6, 12],
   [8, 8, 50, 6, 6, 9999, 0, 8, 8, 8, 8, 8, 8, 50, 0, 0, 8],
   [8, 8, 50, 6, 6, 0, 9999, 8, 8, 8, 8, 8, 8,50, 0, 0, 8],
   [5, 5, 26, 12, 12, 8, 8, 9999, 0, 5, 5, 5, 5, 26, 8, 8, 0],
   [5, 5, 26, 12, 12, 8, 8, 0, 9999, 5, 5, 5, 5, 26, 8, 8, 0],
   [3, 0, 3, 48, 48, 8, 8, 5, 5, 9999, 0, 3, 0, 3, 8, 8, 5],
   [3, 0, 3, 48, 48, 8, 8, 5, 5, 0, 9999, 3, 0, 3, 8, 8, 5],
   [0, 3, 5, 48, 48, 8, 8, 5, 5, 3, 3, 9999, 3, 5, 8, 8, 5],
   [3, 0, 3, 48, 48, 8, 8, 5, 5, 0, 0, 3, 9999, 3, 8, 8, 5],
   [5, 3, 0, 72, 72, 48, 48, 24, 24, 3, 3, 5, 3, 9999, 48, 48, 24],
   [8, 8, 50, 6, 6, 0, 0, 8, 8, 8, 8, 8, 8, 50, 9999, 0, 8],
   [8, 8, 50, 6, 6, 0, 0, 8, 8, 8, 8, 8, 8, 50, 0, 9999, 8],
   [5, 5, 26, 12, 12, 8, 8, 0, 0, 5, 5, 5, 5, 26, 8, 8, 9999]]

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