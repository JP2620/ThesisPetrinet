
# Python program to read
# json file
  
  
import json
import numpy as np
  
# Opening JSON file
f = open('matriz.json')
  
# returns JSON object as 
# a dictionary
data = json.load(f)
matriz_incidencia = data["Incidencia"]
plazas_simples = []
plazas_complejas = []

# Buscamos las plazas con no más de una entrada o salida

for i in range(len(matriz_incidencia)):
    contador_plazas: int = 0
    contador_transiciones: int = 0
    tipos_entradas = {
        1: 0,
        -1: 0
    }
    for j in range(len(matriz_incidencia[0])):
        if (matriz_incidencia[i][j] == 1):
            tipos_entradas[1] += 1
        elif (matriz_incidencia[i][j] == -1):
            tipos_entradas[-1] += 1
    if (not (tipos_entradas[1] > 1 or tipos_entradas[-1] > 1)):
        plazas_simples.append(i + 1)
    else:
        plazas_complejas.append(i + 1)

# Buscamos las transiciones a evitar
transiciones_indeseadas = set()
for j in range(len(matriz_incidencia[0])):
    for i in plazas_complejas:
        if (matriz_incidencia[i - 1][j] != 0):
            transiciones_indeseadas.add(j + 1)

plazas_simples_cpy = plazas_simples.copy()
transiciones_recorridas = []
while (len(plazas_simples_cpy) > 0):
    res = [plazas_simples_cpy[0]]
    for plaza in res:
        plaza_index = plazas_simples_cpy.index(plaza)
        plazas_simples_cpy.pop(plaza_index)
        for t in range(len(matriz_incidencia[plaza - 1])):
            if (matriz_incidencia[plaza - 1][t] != 0 
                    and not t+1 in transiciones_indeseadas
                    and (not t+1 in transiciones_recorridas)):
                transiciones_recorridas.append(t+1)
                for p in range(len(np.transpose(matriz_incidencia)[t])):
                    if (matriz_incidencia[p][t] != 0 and p+1 in plazas_simples_cpy and not p+1 in res):
                        res.append(p + 1)
    print(res)




# Closing file
f.close()






