
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
plazas_dos_entradas_una_salida = []
plazas_dos_salidas_una_entrada = []
plazas_complejas_total = [] #complejas+dosentradas+dossalidas

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
        plazas_complejas_total.append(i + 1)
        if(tipos_entradas[1] == 1 or tipos_entradas[-1] == 1):
            if(tipos_entradas[1] == 2):
                plazas_dos_entradas_una_salida.append(i + 1)
            else:
                plazas_dos_salidas_una_entrada.append(i + 1)
        else:
            plazas_complejas.append(i + 1)

print(plazas_dos_entradas_una_salida)
print(plazas_dos_salidas_una_entrada)
# Buscamos las transiciones a evitar
transiciones_indeseadas = set()
transiciones_indeseadas_totales = set()
transiciones_plazas_dos_entradas_una_salida = []
transiciones_plazas_dos_salidas_una_entrada = []
dict_plazas_dos_entradas_una_salida = {}
dict_plazas_dos_salidas_una_entrada = {}
for j in range(len(matriz_incidencia[0])):
    for i in plazas_complejas:
        if (matriz_incidencia[i - 1][j] != 0):
            transiciones_indeseadas.add(j + 1)
            transiciones_indeseadas_totales.add(j + 1)
    for i in plazas_dos_entradas_una_salida:
        if (matriz_incidencia[i - 1][j] != 0):
            transiciones_indeseadas_totales.add(j + 1)
            transiciones_plazas_dos_entradas_una_salida.append(j + 1)
            dict_plazas_dos_entradas_una_salida[j+1] = (i)
    for i in plazas_dos_salidas_una_entrada:
        if (matriz_incidencia[i - 1][j] != 0):
            transiciones_indeseadas_totales.add(j + 1)
            transiciones_plazas_dos_salidas_una_entrada.append(j + 1)
            dict_plazas_dos_salidas_una_entrada[j+1] = (i)

# Busqueda de trenes sin recursos compartidos
plazas_simples_cpy = plazas_simples.copy()
# transiciones_plazas_dos_entradas_una_salida_cpy = transiciones_plazas_dos_entradas_una_salida.copy()
# transiciones_plazas_dos_salidas_una_entrada = transiciones_plazas_dos_salidas_una_entrada.copy()
transiciones_recorridas = []
caminos_simples_encontrados = []
caminos_con_inicio_fin_complejo_encontrados = []
while (len(plazas_simples_cpy) > 0):
    res = [plazas_simples_cpy[0]]
    res_con_plazas_especiales = [plazas_simples_cpy[0]]
    for plaza in res:
        plaza_index = plazas_simples_cpy.index(plaza)
        plazas_simples_cpy.pop(plaza_index)
        for t in range(len(matriz_incidencia[plaza - 1])):
            if (matriz_incidencia[plaza - 1][t] != 0
                    and (not t+1 in transiciones_recorridas)
                    and (not t+1 in transiciones_indeseadas)):
                transiciones_recorridas.append(t+1)
                if(not t+1 in transiciones_indeseadas_totales):
                    for p in range(len(np.transpose(matriz_incidencia)[t])):
                        if (matriz_incidencia[p][t] != 0 and p+1 in plazas_simples_cpy and not p+1 in res):
                            res.append(p + 1)
                            res_con_plazas_especiales.append(p+1)
                else:
                    if(t+1 in transiciones_plazas_dos_entradas_una_salida and matriz_incidencia[plaza - 1][t] == -1):
                        # transicion_index = transiciones_plazas_dos_entradas_una_salida.index(t+1)
                        # transiciones_plazas_dos_entradas_una_salida.pop(transicion_index)
                        if t+1 in dict_plazas_dos_entradas_una_salida:
                            res_con_plazas_especiales.append(dict_plazas_dos_entradas_una_salida[t+1])
                            # print("A agrego:")
                            # print(dict_plazas_dos_entradas_una_salida[t+1])
                            # print(res)
                            del dict_plazas_dos_entradas_una_salida[t+1]
                    if(t+1 in transiciones_plazas_dos_salidas_una_entrada and matriz_incidencia[plaza - 1][t] == 1):
                        # transicion_index = transiciones_plazas_dos_salidas_una_entrada.index(t+1)
                        # transiciones_plazas_dos_salidas_una_entrada.pop(transicion_index)
                         if t+1 in dict_plazas_dos_entradas_una_salida:
                            res_con_plazas_especiales.append(dict_plazas_dos_salidas_una_entrada[t+1])
                            del dict_plazas_dos_salidas_una_entrada[t+1]

    # print(res)
    caminos_simples_encontrados.append(res)
    caminos_con_inicio_fin_complejo_encontrados.append(res_con_plazas_especiales)
print("Camino simple:")
print(caminos_simples_encontrados)
print("\nCamino con entradas y salidas")
print(caminos_con_inicio_fin_complejo_encontrados)

# Agrega recursos al inicio/final de 2 trenes
# plazas_dos_entradas_una_salida_cpy = plazas_dos_entradas_una_salida.copy()
# plazas_dos_salidas_una_entrada_cpy = plazas_dos_salidas_una_entrada.copy()
# caminos_con_inicio_fin_complejo_encontrados = caminos_simples_encontrados.copy()
# while(len(plazas_dos_entradas_una_salida_cpy) > 0):
#     res = [plazas_dos_entradas_una_salida_cpy[0]]
#     for plaza in res:
#         plaza_index = plazas_dos_entradas_una_salida_cpy.index(plaza)
#         plazas_dos_entradas_una_salida_cpy.pop(plaza_index)
#         for t in range(len(matriz_incidencia[plaza - 1])):
#             if(matriz_incidencia[plaza - 1][t] != 1):


# Closing file
f.close()






