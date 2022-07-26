
# Python program to read
# json file
  
  
import json
from typing import List
import numpy as np
from sqlalchemy import false
  
def clasificar_plazas(matriz_incidencia) -> List[List]:
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
            plazas_simples.append(i + 1) # Guardamos las plazas que tengan como maximo 1 entrada y 1 salida
        else:
            plazas_complejas_total.append(i + 1)
            if(tipos_entradas[1] == 1 or tipos_entradas[-1] == 1):
                if(tipos_entradas[1] == 2):
                    plazas_dos_entradas_una_salida.append(i + 1) # Guardamos las plazas con 2 salidas y 1 entrada maximo
                else:
                    plazas_dos_salidas_una_entrada.append(i + 1) # Guardamos las plazas con 2 entrada y 1 salidas maximo
            else:
                plazas_complejas.append(i + 1)
    
    return [plazas_simples, plazas_complejas, plazas_dos_entradas_una_salida, plazas_dos_salidas_una_entrada, plazas_complejas_total]

# Opening JSON file
f = open('matriz.json')
  
# returns JSON object as 
# a dictionary
data = json.load(f)
matriz_incidencia = data["Incidencia"]

# Buscamos las plazas con no más de una entrada o salida
plazas_simples,\
plazas_complejas,\
plazas_dos_entradas_una_salida,\
plazas_dos_salidas_una_entrada,\
plazas_complejas_total = clasificar_plazas(matriz_incidencia)

print(plazas_dos_entradas_una_salida)
print(plazas_dos_salidas_una_entrada)
print(plazas_complejas)


# Buscamos las transiciones a evitar y tambien guardamos unos keymap de:
# *) Transicion relacionada con la salida  con plazas_dos_entradas_una_salida
# *) Transicion relacionada con la entrada con plazas_dos_salidas_una_entrada
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



# Busco los trenes comprendidos por:
#  *) Caminos simples (plazas con 1 entrada y 1 salida)
#  *) Recursos internos
#  *) plazas de 1 in y 2 out y 2 in y 1 out
plazas_simples_cpy = plazas_simples.copy()
plazas_dos_entradas_una_salida_cpy = plazas_dos_entradas_una_salida.copy()
plazas_dos_salidas_una_entrada_cpy = plazas_dos_salidas_una_entrada.copy()
transiciones_recorridas = []
caminos_simples_encontrados = []
caminos_con_inicio_fin_complejo_encontrados = []
transiciones_de_caminos_simples_encontrados = []
transiciones_de_caminos_con_inicio_fin_complejo_encontrados = []
transiciones_borde = transiciones_indeseadas_totales.copy()
while (len(plazas_simples_cpy) > 0): # Voy a intentar recorrer todas las plazas de 1 entrda y 1 salida
    res = [plazas_simples_cpy[0]] # Guardo la primera plaza
    res_transiciones_usadas = set()
    res_con_plazas_especiales = [plazas_simples_cpy[0]]
    res_transiciones_usadas_con_plazas_especiales = set()
    for plaza in res: #recorro todas las plazas de res para buscar plazas conectadas a esta y agregarlas al mismo
        plaza_index = plazas_simples_cpy.index(plaza)
        plazas_simples_cpy.pop(plaza_index)
        for t in range(len(matriz_incidencia[plaza - 1])):
            if (matriz_incidencia[plaza - 1][t] != 0): # Si es distinto de 0 significa que esta T esta conectada a la plaza que estoy analizando
                res_transiciones_usadas_con_plazas_especiales.add(t+1)
                res_transiciones_usadas.add(t+1)
                if (not t+1 in transiciones_recorridas): # Solo me interesa si no la recorri
                    if (not t+1 in transiciones_indeseadas): 
                        transiciones_recorridas.append(t+1)
                        if(not t+1 in transiciones_indeseadas_totales): # Si la transicion tiene max 1 entrada/salida o es de un recurso interno busco las plazas atadas a esta
                            for p in range(len(np.transpose(matriz_incidencia)[t])):
                                if (matriz_incidencia[p][t] != 0 and p+1 in plazas_simples_cpy and not p+1 in res): # Si la plaza esta conectado a esta transicion, es simple (1 in/out max) y no esta en res
                                    res.append(p + 1)
                                    res_con_plazas_especiales.append(p+1)
                        else:
                            if(t+1 in transiciones_plazas_dos_entradas_una_salida and matriz_incidencia[plaza - 1][t] == -1):
                                # transicion_index = transiciones_plazas_dos_entradas_una_salida.index(t+1)
                                # transiciones_plazas_dos_entradas_una_salida.pop(transicion_index)
                                if t+1 in dict_plazas_dos_entradas_una_salida:
                                    if dict_plazas_dos_entradas_una_salida[t+1] in plazas_dos_entradas_una_salida_cpy:
                                        transiciones_borde.remove(t+1)
                                        plaza_index = plazas_dos_entradas_una_salida_cpy.index(dict_plazas_dos_entradas_una_salida[t+1])
                                        plazas_dos_entradas_una_salida_cpy.pop(plaza_index)
                                        res_con_plazas_especiales.append(dict_plazas_dos_entradas_una_salida[t+1])
                                        for tt in range(len(matriz_incidencia[dict_plazas_dos_entradas_una_salida[t+1] - 1])):
                                            if(tt != t and matriz_incidencia[dict_plazas_dos_entradas_una_salida[t+1] - 1][tt] != 0):
                                                res_transiciones_usadas_con_plazas_especiales.add(tt+1)
                                    # print("A agrego:")
                                    # print(dict_plazas_dos_entradas_una_salida[t+1])
                                    # print(res)
                                    del dict_plazas_dos_entradas_una_salida[t+1]
                            if(t+1 in transiciones_plazas_dos_salidas_una_entrada and matriz_incidencia[plaza - 1][t] == 1):
                                # transicion_index = transiciones_plazas_dos_salidas_una_entrada.index(t+1)
                                # transiciones_plazas_dos_salidas_una_entrada.pop(transicion_index)
                                if t+1 in dict_plazas_dos_salidas_una_entrada:
                                    if dict_plazas_dos_salidas_una_entrada[t+1] in plazas_dos_salidas_una_entrada_cpy:
                                        transiciones_borde.remove(t+1)
                                        plaza_index = plazas_dos_salidas_una_entrada_cpy.index(dict_plazas_dos_salidas_una_entrada[t+1])
                                        plazas_dos_salidas_una_entrada_cpy.pop(plaza_index)
                                        res_con_plazas_especiales.append(dict_plazas_dos_salidas_una_entrada[t+1])
                                        for tt in range(len(matriz_incidencia[dict_plazas_dos_salidas_una_entrada[t+1] - 1])):
                                            if(tt != t and matriz_incidencia[dict_plazas_dos_salidas_una_entrada[t+1] - 1][tt] != 0):
                                                res_transiciones_usadas_con_plazas_especiales.add(tt+1)
                                    del dict_plazas_dos_salidas_una_entrada[t+1]
                    else: # No recurrida pero conectada a un recurso compartido
                        for p in range(len(np.transpose(matriz_incidencia)[t])):
                                if (matriz_incidencia[p][t] != 0 and p+1 in plazas_simples_cpy and not p+1 in res): # Si la plaza esta conectado a esta transicion, es simple (1 in/out max) y no esta en res
                                    res.append(p + 1)
                                    res_con_plazas_especiales.append(p+1)
                                    transiciones_borde.add(t+1)

    caminos_simples_encontrados.append(res)
    caminos_con_inicio_fin_complejo_encontrados.append(res_con_plazas_especiales)
    transiciones_de_caminos_simples_encontrados.append(res_transiciones_usadas)
    transiciones_de_caminos_con_inicio_fin_complejo_encontrados.append(res_transiciones_usadas_con_plazas_especiales)


# Agrega recursos compartidos
for p in plazas_complejas:
    encontro = False
    transiciones_conectadas = set()
    for t in range(len(matriz_incidencia[p-1])):
        if matriz_incidencia[p-1][t] != 0:
            transiciones_conectadas.add(t+1)
    for t_conjunto in range(len(transiciones_de_caminos_con_inicio_fin_complejo_encontrados)):
        cantidad_encontradas = 0
        temp = []
        temp2 = []
        for tplaza in transiciones_conectadas:
            if tplaza in transiciones_de_caminos_con_inicio_fin_complejo_encontrados[t_conjunto]:
                cantidad_encontradas+=1
                temp2.append(tplaza)
            else:
                temp.append(tplaza)
        if cantidad_encontradas > 1:
            encontro = True
            print("Deberia agregar la plaza", p, "en el arreglo", caminos_con_inicio_fin_complejo_encontrados[t_conjunto], "y", temp, "en ", transiciones_de_caminos_con_inicio_fin_complejo_encontrados[t_conjunto])
            caminos_con_inicio_fin_complejo_encontrados[t_conjunto].append(p)
            for t_faltantes in temp:
                transiciones_de_caminos_con_inicio_fin_complejo_encontrados[t_conjunto].add(t_faltantes)
            for t_no_faltantes in temp2:
                transiciones_borde.remove(t_no_faltantes)
                for p_conectados in range(len(np.transpose(matriz_incidencia)[t_no_faltantes-1])):
                    if(matriz_incidencia[p_conectados-1][t_no_faltantes-1] != 0 and not p_conectados+1 in caminos_con_inicio_fin_complejo_encontrados[t_conjunto]):
                        transiciones_borde.add(t_no_faltantes) # Si hay alguna plaza que no forme parte del subconujunto agrego la transicion como borde
            print("Deberia agregar la plaza", p, "en el arreglo", caminos_con_inicio_fin_complejo_encontrados[t_conjunto], "y", temp, "en ", transiciones_de_caminos_con_inicio_fin_complejo_encontrados[t_conjunto])
            break
    if not encontro:
        caminos_con_inicio_fin_complejo_encontrados.append([p])
        transiciones_de_caminos_con_inicio_fin_complejo_encontrados.append(transiciones_conectadas)

            


# Obtengo la matriz incidencias
matriz_incidencia_caminos_complejos = []
for numero_camino in range(len(caminos_simples_encontrados)):
    temp_padre = []
    for indice_p in range(len(caminos_con_inicio_fin_complejo_encontrados[numero_camino])):
        temp = []
        for t in transiciones_de_caminos_con_inicio_fin_complejo_encontrados[numero_camino]:
           temp.append(matriz_incidencia[caminos_con_inicio_fin_complejo_encontrados[numero_camino][indice_p] - 1][t-1])
        temp_padre.append(temp)
    matriz_incidencia_caminos_complejos.append(temp_padre)
    print("")

# Calculo Matriz Relacion:
matriz_relacion = []
for conjunto in transiciones_de_caminos_con_inicio_fin_complejo_encontrados:
    temp = []
    for t in transiciones_borde:
        if t in conjunto:
            temp.append(1)
        else:
            temp.append(0)
    matriz_relacion.append(temp)


print("\nCamino con matriz_relacionentradas y salidas:")
print("Plazas:",caminos_con_inicio_fin_complejo_encontrados)
print("Transiciones:", transiciones_de_caminos_con_inicio_fin_complejo_encontrados)
print("M Incidencia:",matriz_incidencia_caminos_complejos)
# print("Tamaño matriz relacion", len(transiciones_borde), "x", len(caminos_con_inicio_fin_complejo_encontrados))
print("Transiciones borde", transiciones_borde)
print("Matriz relacion", matriz_relacion)

# Closing file
f.close()






