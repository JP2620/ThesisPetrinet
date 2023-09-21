
# Python program to read
# json file
  
  
import json
from typing import List, Any
from os import listdir, system
from os.path import isfile, join
from itertools import compress, product
import numpy as np
import re
import copy

PATH_MINCOV = "./salida2/PetrinetSE-original"

""" Entra set() sale <elemento1>-<elemento1><elemento1>-<elemento1> """
def set_to_string(items):
    string_set = '-'.join(list([str(num) for num in items]))
    return string_set

# take a list of int and return a string with the following format
# [0, 1, 2, 3] -> "[0, 1, 2, 3 ]"

def list_to_string(lista: List[int]) -> str:
    return "[" + ", ".join([str(elem) for elem in lista]) + " ]"

  
def combinations(items):
    return ( set(compress(items,mask)) for mask in product(*[[0,1]]*len(items)) )

def clasificar_plazas(matriz_incidencia) -> List[List]:
    plazas_simples = []
    plazas_complejas = []
    plazas_dos_entradas_una_salida = []
    plazas_dos_salidas_una_entrada = []
    plazas_complejas_total = [] #complejas+dosentradas+dossalidas

    # Buscamos las plazas con no más de una entrada o salida
    for i in range(N_PLAZAS):
        contador_plazas: int = 0
        contador_transiciones: int = 0
        tipos_entradas = {
            1: 0,
            -1: 0
        }
        for j in range(N_TRANSICIONES):
            if (matriz_incidencia[i][j] > 0):
                tipos_entradas[1] += 1
            elif (matriz_incidencia[i][j] < 0):
                tipos_entradas[-1] += 1
        if (not (tipos_entradas[1] > 1 or tipos_entradas[-1] > 1)):
            plazas_simples.append(i + 1) # Guardamos las plazas que tengan como maximo 1 entrada y 1 salida
        else:
            plazas_complejas_total.append(i + 1)
            if(tipos_entradas[1] <= 1 or tipos_entradas[-1] <= 1):
                if(tipos_entradas[1] == 2):
                    plazas_dos_entradas_una_salida.append(i + 1) # Guardamos las plazas con 2 salidas y 1 entrada maximo
                else:
                    plazas_dos_salidas_una_entrada.append(i + 1) # Guardamos las plazas con 2 entrada y 1 salidas maximo
            else:
                plazas_complejas.append(i + 1)
    
    return [plazas_simples, plazas_complejas, plazas_dos_entradas_una_salida, plazas_dos_salidas_una_entrada, plazas_complejas_total]

"""
La transición está conectada a una plaza con 2i1o o 1i2o 
Esta funcion intenta conectar el tren normal (camino simple + recurso propio) con las plazas con 2i1o o 1i2o 
"""
def try_add_to_train_2i1o_1i2o(t,res_con_plazas_especiales,res_transiciones_usadas_con_plazas_especiales) -> None:
    if (t+1 in transiciones_plazas_dos_entradas_una_salida 
            and t+1 in dict_plazas_dos_entradas_una_salida
            and dict_plazas_dos_entradas_una_salida[t+1] in plazas_dos_entradas_una_salida
            and matriz_incidencia[dict_plazas_dos_entradas_una_salida[t+1] - 1][t] > 0): # Si es de entrada
        plaza_dos_entradas_una_salida = dict_plazas_dos_entradas_una_salida[t+1]
        transiciones_borde.remove(t+1)
        plaza_index = plazas_dos_entradas_una_salida.index(plaza_dos_entradas_una_salida)
        plazas_dos_entradas_una_salida.pop(plaza_index)
        res_con_plazas_especiales.append(plaza_dos_entradas_una_salida)
        for tt in range(N_TRANSICIONES):
            if(tt != t and matriz_incidencia[plaza_dos_entradas_una_salida - 1][tt] != 0):
                res_transiciones_usadas_con_plazas_especiales.add(tt+1)
        del plaza_dos_entradas_una_salida
    if(t+1 in transiciones_plazas_dos_salidas_una_entrada
            and t+1 in dict_plazas_dos_salidas_una_entrada
            and dict_plazas_dos_salidas_una_entrada[t+1] in plazas_dos_salidas_una_entrada
            and matriz_incidencia[dict_plazas_dos_salidas_una_entrada[t+1]- 1][t] < 0):
        plaza_dos_salidas_una_entrada = dict_plazas_dos_salidas_una_entrada[t+1]
        transiciones_borde.remove(t+1)
        plaza_index = plazas_dos_salidas_una_entrada.index(plaza_dos_salidas_una_entrada)
        plazas_dos_salidas_una_entrada.pop(plaza_index)
        res_con_plazas_especiales.append(plaza_dos_salidas_una_entrada)
        for tt in range(N_TRANSICIONES):
            if(tt != t and matriz_incidencia[plaza_dos_salidas_una_entrada - 1][tt] != 0):
                res_transiciones_usadas_con_plazas_especiales.add(tt+1)
        del plaza_dos_salidas_una_entrada

def generate_mincov_json_input_general(matriz) -> str:
    salida_filename = "./salida/matriz_incidencia_.json"
    with open(salida_filename, "w") as f:
        file = {}
        plazas = []
        transiciones = []
        arcos = []
        for j, columna in enumerate(matriz[0]):
            transicion = {
                "index": j,
                "type": "immediate",
                "guard": True,
                "event": True,
            }
            transiciones.append(transicion)
        for j, fila in enumerate(matriz):
            # Create json object
            plaza = {
                "index": j,
                "type": "discrete",
                "initial_marking": marcado_inicial[j],
            }
            plazas.append(plaza)
            for k, columna in enumerate(fila):
                if columna > 0:
                    arco = {
                        "type": "regular",
                        "from_place": False, 
                        "source": k,
                        "target": j,
                        "weight": columna,
                    }
                    arcos.append(arco)
                elif columna < 0:
                    arco = {
                        "type": "regular",
                        "from_place": True, 
                        "source": j,
                        "target": k,
                        "weight": -columna,
                    }
                    arcos.append(arco)
                
        file["places"] = plazas
        file["transitions"] = transiciones
        file["arcs"] = arcos

        network = {
            "id": "ejemplo",
            "amount_places": len(plazas),
            "amount_transitions": len(transiciones),
            "time_scale": "millisecond",
            "is_temporal": False,
            "network_type": "discrete",
        }
        file["network"] = network
        f.write(json.dumps(file))
        return salida_filename

def join_tree(arbol_de_alcanzabilidad, cantidad_plazas: int):
    nodos = {}
    conexiones = []
    for subred_padre in arbol_de_alcanzabilidad:
        for subred_hija in subred_padre:
            if len(subred_padre[subred_hija]["nodos"][next(iter(subred_padre[subred_hija]["nodos"]))]) == cantidad_plazas:
                print("COMPLETO: ", subred_padre[subred_hija]["nodos"])
                nodos = nodos | subred_padre[subred_hija]["nodos"]
                conexiones += subred_padre[subred_hija]["conexiones"]
    return {"nodos" : nodos, "conexiones" : conexiones}


def generate_mincov_json_filled2(arbol_de_alcanzabilidad):
    # print(key, arbol_de_alcanzabilidad[key])
    # print("\n--------------SOY UN SEPARADOR--------------\n")
    new_filename = "./salida/mincov_filled_out_final.json"
    with open(new_filename, "w") as f:
        file = {}
        file["network"] = "red_final"
        file["nodes"] = []
        file["edges"] = []
        for key2 in arbol_de_alcanzabilidad["nodos"]:
            # print(key, key2)
            # print(arbol_de_alcanzabilidad[key]["nodos"][key2])
            # print(list_to_string(arbol_de_alcanzabilidad[key]["nodos"][key2]))
            file["nodes"].append({
                    "id": "n" + str(key2),
                    "state": list_to_string(arbol_de_alcanzabilidad["nodos"][key2]),
                    "group": "root" if key2 == 1 else "not omega",
                })
        for key3 in arbol_de_alcanzabilidad["conexiones"]:
            file["edges"].append({
                "from": "n" + str(key3[0]),
                "path": "n" + str(key3[0]) + " --(T" + str(key3[1]) + ")--> n" + str(key3[2]),
                "to": "n" + str(key3[2]),
            })

        f.write(json.dumps(file))

def generate_mincov_json_filled(arbol_de_alcanzabilidad, red_id):
    for key in arbol_de_alcanzabilidad:
        # print(key, arbol_de_alcanzabilidad[key])
        # print("\n--------------SOY UN SEPARADOR--------------\n")
        new_filename = "./salida/mincov_filled_out_" + str(red_id) + "_" +str(key) + ".json"
        with open(new_filename, "w") as f:
            file = {}
            file["network"] = "red_" + str(key)
            file["nodes"] = []
            file["edges"] = []
            for key2 in arbol_de_alcanzabilidad[key]["nodos"]:
                # print(key, key2)
                # print(arbol_de_alcanzabilidad[key]["nodos"][key2])
                # print(list_to_string(arbol_de_alcanzabilidad[key]["nodos"][key2]))
                file["nodes"].append({
                        "id": "n" + str(key2),
                        "state": list_to_string(arbol_de_alcanzabilidad[key]["nodos"][key2]),
                        "group": "root" if key2 == 1 else "not omega",
                    })
            for key3 in arbol_de_alcanzabilidad[key]["conexiones"]:
                file["edges"].append({
                    "from": "n" + str(key3[0]),
                    "path": "n" + str(key3[0]) + " --(T" + str(key3[1]) + ")--> n" + str(key3[2]),
                    "to": "n" + str(key3[2]),
                })

            f.write(json.dumps(file))


def generate_mincov_json_input (i, matriz, plazas_temp_con_mark) -> str:
    new_filename = "./salida/matriz_incidencia_" + str(i) + "_" + set_to_string(plazas_temp_con_mark) + ".json"
    with open(new_filename, "w") as f:
        file = {}
        plazas = []
        transiciones = []
        arcos = []
        for j, columna in enumerate(matriz[0]):
            transicion = {
                "index": j,
                "type": "immediate",
                "guard": True,
                "event": True,
            }
            transiciones.append(transicion)
        for j, fila in enumerate(matriz):
            # Create json object
            plaza_a_verificar = caminos_con_inicio_fin_complejo_encontrados[i][j]
            if plaza_a_verificar < 0: #significa que es una aux
                if plaza_a_verificar*-1 in plazas_temp_con_mark:
                    plaza = {
                        "index": j,
                        "type": "discrete",
                        "initial_marking":1,
                    }
                else:
                    plaza = {
                        "index": j,
                        "type": "discrete",
                        "initial_marking":0,
                    }
            else:
                plaza = {
                    "index": j,
                    "type": "discrete",
                    "initial_marking": marcado_inicial[caminos_con_inicio_fin_complejo_encontrados[i][j] - 1],
                }
            plazas.append(plaza)
            for k, columna in enumerate(fila):
                if columna > 0:
                    arco = {
                        "type": "regular",
                        "from_place": False, 
                        "source": k,
                        "target": j,
                        "weight": columna,
                    }
                    arcos.append(arco)
                elif columna < 0:
                    arco = {
                        "type": "regular",
                        "from_place": True, 
                        "source": j,
                        "target": k,
                        "weight": -columna,
                    }
                    arcos.append(arco)
                
        file["places"] = plazas
        file["transitions"] = transiciones
        file["arcs"] = arcos

        network = {
            "id": "ejemplo",
            "amount_places": len(plazas),
            "amount_transitions": len(transiciones),
            "time_scale": "millisecond",
            "is_temporal": False,
            "network_type": "discrete",
        }
        file["network"] = network
        f.write(json.dumps(file))
    return new_filename

# Opening JSON file
f = open('matriz.json')
  
# returns JSON object as 
# a dictionary
data = json.load(f)
matriz_incidencia = data["Incidencia"]
matriz_incidencia_transpuesta = np.transpose(matriz_incidencia)
marcado_inicial = data["Marcado"]

N_PLAZAS = len(matriz_incidencia)
N_TRANSICIONES = len(matriz_incidencia[0])

# Buscamos las plazas con no más de una entrada o salida
plazas_simples,\
plazas_complejas,\
plazas_dos_entradas_una_salida,\
plazas_dos_salidas_una_entrada,\
plazas_complejas_total = clasificar_plazas(matriz_incidencia)

# print(plazas_dos_entradas_una_salida)
# print(plazas_dos_salidas_una_entrada)
# print(plazas_complejas)


# Buscamos las transiciones a evitar y tambien guardamos unos keymap de:
# *) Transicion relacionada con la salida  con plazas_dos_entradas_una_salida
# *) Transicion relacionada con la entrada con plazas_dos_salidas_una_entrada
transiciones_indeseadas = set()
transiciones_indeseadas_totales = set()
transiciones_plazas_dos_entradas_una_salida = []
transiciones_plazas_dos_salidas_una_entrada = []
dict_plazas_dos_entradas_una_salida = {}
dict_plazas_dos_salidas_una_entrada = {}
for j in range(N_TRANSICIONES):
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
transiciones_recorridas = []
caminos_simples_encontrados = []
caminos_con_inicio_fin_complejo_encontrados = []
transiciones_de_caminos_simples_encontrados = []
transiciones_de_caminos_con_inicio_fin_complejo_encontrados = []
transiciones_borde = transiciones_indeseadas_totales.copy()
while (len(plazas_simples) > 0): # Voy a intentar recorrer todas las plazas de 1 entrda y 1 salida
    res = [plazas_simples[0]] # Guardo la primera plaza
    res_transiciones_usadas = set()
    res_con_plazas_especiales = [plazas_simples[0]] # plazas especiales son aquellas con 2 entradas y 1 salida mazimo o viceversa 
    res_transiciones_usadas_con_plazas_especiales = set()
    for plaza in res: #recorro todas las plazas de res para buscar plazas conectadas a esta y agregarlas al mismo
        plaza_index = plazas_simples.index(plaza)
        plazas_simples.pop(plaza_index)
        for t in range(N_TRANSICIONES):
            if (matriz_incidencia[plaza - 1][t] != 0): # Si es distinto de 0 significa que esta T esta conectada a la plaza que estoy analizando
                res_transiciones_usadas_con_plazas_especiales.add(t+1)
                res_transiciones_usadas.add(t+1)
                if (not t+1 in transiciones_recorridas): # Solo me interesa si no la recorri
                    if (not t+1 in transiciones_indeseadas): # La transicion no sea de un recurso compartido
                        transiciones_recorridas.append(t+1)
                        if(not t+1 in transiciones_indeseadas_totales): # Si la transicion tiene max 1 entrada/salida o es de un recurso interno busco las plazas atadas a esta
                            for p in range(N_PLAZAS):
                                if (matriz_incidencia[p][t] != 0 and p+1 in plazas_simples and not p+1 in res): # Si la plaza esta conectado a esta transicion, es simple (1 in/out max) y no esta en res
                                    res.append(p + 1)
                                    res_con_plazas_especiales.append(p+1)
                        # Significa que la transicion esta conectada a una plaza de 2i1o o 2o1i
                        else:
                            try_add_to_train_2i1o_1i2o(t,res_con_plazas_especiales,res_transiciones_usadas_con_plazas_especiales)
                    else: # No recurrida pero conectada a un recurso compartido
                        for p in range(N_PLAZAS):
                                # Si la plaza esta conectado a esta transicion, es simple (1 in/out max) y no esta en res
                                if (matriz_incidencia[p][t] != 0 and p+1 in plazas_simples and not p+1 in res): 
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
    for t in range(N_TRANSICIONES):
        if matriz_incidencia[p-1][t] != 0:
            transiciones_conectadas.add(t+1) # Guarda transiciones conectadas al recurso compartido
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
            # print("Deberia agregar la plaza", p, "en el arreglo", caminos_con_inicio_fin_complejo_encontrados[t_conjunto], "y", temp, "en ", transiciones_de_caminos_con_inicio_fin_complejo_encontrados[t_conjunto])
            caminos_con_inicio_fin_complejo_encontrados[t_conjunto].append(p)
            for t_faltantes in temp:
                transiciones_de_caminos_con_inicio_fin_complejo_encontrados[t_conjunto].add(t_faltantes)
            for t_no_faltantes in temp2:
                transiciones_borde.remove(t_no_faltantes)
                for p_conectados in range(N_PLAZAS):
                    if(matriz_incidencia[p_conectados-1][t_no_faltantes-1] != 0 and not p_conectados+1 in caminos_con_inicio_fin_complejo_encontrados[t_conjunto]):
                        transiciones_borde.add(t_no_faltantes) # Si hay alguna plaza que no forme parte del subconujunto agrego la transicion como borde
            # print("Deberia agregar la plaza", p, "en el arreglo", caminos_con_inicio_fin_complejo_encontrados[t_conjunto], "y", temp, "en ", transiciones_de_caminos_con_inicio_fin_complejo_encontrados[t_conjunto])
            break
    if not encontro:
        caminos_con_inicio_fin_complejo_encontrados.append([p])
        transiciones_de_caminos_con_inicio_fin_complejo_encontrados.append(transiciones_conectadas)

            
# Calculo Matriz Relacion:
matriz_relacion = [] # 1 columna por transicion borde y 1 fila por subred
transiciones_con_plazas_aux = []
transiciones_borde = list(transiciones_borde)
for i, conjunto in enumerate(transiciones_de_caminos_con_inicio_fin_complejo_encontrados):
    temp = []
    temp_transiciones_con_plazas_aux = []
    for t in transiciones_borde:
        if t in conjunto:
            temp.append(1)
            for p in range(N_PLAZAS):
                if matriz_incidencia[p][t-1] < 0 and not p+1 in caminos_con_inicio_fin_complejo_encontrados[i]:
                    temp_transiciones_con_plazas_aux.append(t)
                    break
        else:
            temp.append(0)
    matriz_relacion.append(temp)
    transiciones_con_plazas_aux.append(temp_transiciones_con_plazas_aux)


# Obtengo la matriz incidencias
matriz_incidencia_caminos_complejos = []
for numero_camino in range(len(caminos_simples_encontrados)):
    temp_padre = []
    for indice_p in range(len(caminos_con_inicio_fin_complejo_encontrados[numero_camino])):
        temp = []
        for t in transiciones_de_caminos_con_inicio_fin_complejo_encontrados[numero_camino]:
           temp.append(matriz_incidencia[caminos_con_inicio_fin_complejo_encontrados[numero_camino][indice_p] - 1][t-1])
        temp_padre.append(temp)
    for tt in transiciones_con_plazas_aux[numero_camino]:
        temp = []
        for t in transiciones_de_caminos_con_inicio_fin_complejo_encontrados[numero_camino]:
            if t==tt:
                temp.append(-1)
            else:
                temp.append(0)
        temp_padre.append(temp)
        caminos_con_inicio_fin_complejo_encontrados[numero_camino].append(tt*-1)
    matriz_incidencia_caminos_complejos.append(temp_padre)
    # print("")

# TODO: Ver si en un futuro se puede hacer que transiciones_de_caminos_con_inicio_fin_complejo_encontrados contenga lista)
for i, transiciones in enumerate(transiciones_de_caminos_con_inicio_fin_complejo_encontrados):
    transiciones_de_caminos_con_inicio_fin_complejo_encontrados[i] = list(transiciones)

print("Marcado Inicial:",marcado_inicial)
print("\nCamino con matriz_relacionentradas y salidas:")
print("Plazas:",caminos_con_inicio_fin_complejo_encontrados)
print("Transiciones:", transiciones_de_caminos_con_inicio_fin_complejo_encontrados)
print("M Incidencia:",matriz_incidencia_caminos_complejos)
# print("Tamaño matriz relacion", len(transiciones_borde), "x", len(caminos_con_inicio_fin_complejo_encontrados))
print("Transiciones borde", transiciones_borde)
print("Matriz relacion", matriz_relacion)
print("Plazas aux", transiciones_con_plazas_aux)

# Closing file
f.close()
print("\n--------------SOY UN SEPARADOR--------------\n")



"""
matriz_incidencia_... son entradas del algoritmo de gabi
- Ejecutar algoritmo de gabi con cada una de esas entradas
- Renombrar salidas del algoritmo de gabi con el patrón mincov_out_...etc
"""

mincov_inputs = []
for i, matriz in enumerate(matriz_incidencia_caminos_complejos):
    mincov_inputs.append(generate_mincov_json_input(i,matriz, set()))
    for plazas_temp_con_mark in combinations(transiciones_con_plazas_aux[i]):
        if len(plazas_temp_con_mark) > 0:
            set_to_string(plazas_temp_con_mark)
            mincov_input_filename = generate_mincov_json_input(i,matriz, plazas_temp_con_mark)
            mincov_inputs.append(mincov_input_filename)
mincov_inputs.append(generate_mincov_json_input_general(matriz_incidencia))



for mincov_input in mincov_inputs:
    system(f"{PATH_MINCOV} -a {mincov_input} > /dev/null")
    sufix = re.search(r".*incidencia_(.*)", mincov_input).groups()[0]
    system(f"mv ./mincov_out.json ./salida/mincov_out_{sufix}.json ")







"""
Quiero que el programa me guarde una lista por cada subred que a
su vez tenga una lista por cada combinacion de salida (las 
combinaciones se dan si tiene plaza auxiliares ya que estas pueden
estar habilitadas o deshabilitadas). Dentro de esta ultima lista 
necesito todos los estados de la salidas y sus respectivas relaciones
"""

def stateToList(state: str) -> List[int]:
    a = state.split(" ")[:-1]
    a[0] = a[0][1:]
    a = [int(x) for x in a]
    return a

def getArbolFromSalida(s: str, numero_sub_red: int, index_nodos: int, is_none: bool):
    with open(f"salida/{s}") as salida:
        # if not is_none and index_nodos > 0:
        #     index_nodos += 1
        salida_json = json.load(salida)
        array_nodos = {} # n1 = [0,0,1,0] va a ser {1: [0,0,1,0]}
        array_conexiones = [] # n1 -> t5 -> n2 va a ser [1,5,2]
        conexiones_agregadas = set()

        for nodes in salida_json["nodes"]:
            n = int(nodes["id"][1:])
            if n!=1 or not is_none:
                n += index_nodos
            state = stateToList(nodes["state"])
            array_nodos[n] = state

        for conexiones in salida_json["edges"]:
            n = conexiones["path"]
            if n not in conexiones_agregadas:
                conexiones_agregadas.add(n)
                temp = []
                nodo_from = int(conexiones["from"][1:])
                if nodo_from != 1 or not is_none:
                    nodo_from += index_nodos
                nodo_to = int(conexiones["to"][1:])
                if nodo_to != 1 or not is_none:
                    nodo_to += index_nodos
                temp.append(nodo_from)
                temp.append(transiciones_de_caminos_con_inicio_fin_complejo_encontrados[numero_sub_red][int(re.search(r".*T(\d+)", n).groups()[0])-1])
                temp.append(nodo_to)
                array_conexiones.append(temp)
        new_index_nodos = index_nodos + len(array_nodos) + 1
        if is_none and len(array_nodos) == 1:
            new_index_nodos -= 1
        print("len", len(array_nodos))
        print("new_index_nodos", new_index_nodos)
        print("proximo", new_index_nodos + len(array_nodos))
        return {"nodos" : array_nodos, "conexiones": array_conexiones, "completo" : False}, new_index_nodos-1


PREFIX = "mincov_out_"
salidasMinCov = [f for f in sorted(listdir("salida")) if f.find(PREFIX) != -1]
lista_arboles_de_alcanzabilidad = []

index_nodos = 0
for i, subred in enumerate(caminos_con_inicio_fin_complejo_encontrados):
    salidas_de_la_subred = [s for s in salidasMinCov if s.startswith(f"{PREFIX}{i}")]
    if len(salidas_de_la_subred) > 0:
        lista_arboles_de_alcanzabilidad.append({})
        arboles = lista_arboles_de_alcanzabilidad[i]

        for s in salidas_de_la_subred:
            plazas_aux_con_marcadoinicial = s[s.index(str(i))+2:].split(".")[0]
            identificador_posibilidad = plazas_aux_con_marcadoinicial if plazas_aux_con_marcadoinicial != "" else "none"
            arboles[identificador_posibilidad], index_nodos  = getArbolFromSalida(s, i, index_nodos, identificador_posibilidad=="none")

# print("aca empieza")
print(lista_arboles_de_alcanzabilidad)
print("\n--------------SOY UN SEPARADOR--------------\n")

def completarNodo(lista_nodos_subred, lista_orden_plazas_subred, marcado_incial):
    lista_nodos_subred_cpy = copy.deepcopy(lista_nodos_subred)
    for i in range(N_PLAZAS):
        if i+1 in lista_orden_plazas_subred: ## Si la plaza i existe en mi red guardo el valor de esta
            posicion = lista_orden_plazas_subred.index(i+1) ## Guardo la posicion local de la plaza global i
            for nodos in lista_nodos_subred: ## nodos me esta devolviendo las key que seria 1..n
                nodo = lista_nodos_subred[nodos] ## guardo el value de esa key osea el marcado de ese nodo
                nodo_cpy = lista_nodos_subred_cpy[nodos]
                if i < len(nodo): ## Aca quiero completarla por lo que si todavia me queda lugar lo sobreescribo
                    nodo[i] = nodo_cpy[posicion]
                else: # Si no me queda lugar lo agrego
                    nodo.append(nodo_cpy[posicion])
        else: # Si no existe esa plaza i en mi vectr, tomo el valor del marcado inicial
            for nodos in lista_nodos_subred:
                nodo = lista_nodos_subred[nodos]
                if i < len(nodo):
                    nodo[i] = marcado_incial[i]
                else:
                    nodo.append(marcado_incial[i])
    for nodo in lista_nodos_subred: # Voy a retorna el nodo si este es el nodo original
        if lista_nodos_subred[nodo] == marcado_incial:
            return nodo
    return -1

def buscarMarcadoDeseado(lista_nodos_subred, plaza_con_marcado_deseada): # Solo busca el primer marcarcado
    lista_nodos_subred_cpy = copy.deepcopy(lista_nodos_subred)
    lista_marcados_posibles = []
    nodo_que_conecta = -1
    for key, nodo in lista_nodos_subred.items():
        conecta = True
        for p in plaza_con_marcado_deseada:
            if nodo[p] < 1: #TODO: RESISAR QUE PASA CON W
                conecta = False
                break
            else:
                lista_nodos_subred_cpy[key][p] -= 1
            # ANTES TIENE QUE ELIMINAR UN MARCADO DE ESTA PLAZA
        if conecta: 
            nodo_que_conecta = key
            lista_marcados_posibles.append(lista_nodos_subred_cpy[key])
    return lista_marcados_posibles, nodo_que_conecta


def procesarSubredRelacionada(indice):
    for indice_mr, valor in enumerate(matriz_relacion[indice]):
        if valor == 1:
            for indice_red, red in enumerate(matriz_relacion): ## aca puedo recorer hasta indice total despues se ven las otras
                if indice_red != indice and red[indice_mr] == 1:
                    completarSubred(indice_red, lista_arboles_de_alcanzabilidad[indice_red])
                    break

def completarSubred(indice, subred):
    completeuna = False
    for plazas_aux in subred:
        if subred[plazas_aux]["completo"] == False: # Solo reviso las que no complete
            if "none" in plazas_aux:
                completarNodo(subred[plazas_aux]["nodos"], caminos_con_inicio_fin_complejo_encontrados[indice], marcado_inicial)
                completeuna = True
                subred["none"]["completo"] = True
            else:
                transicones_compartidas = []
                if "-" in plazas_aux: # TODO: Seguro se puede mejorar. En las plaza_aux no none, tengo el nombre de las transiciones compartidas activas separadas con guion medio
                    transiciones_compartidas_strings = plazas_aux.split("-")
                    for transcion_compartida_string in transiciones_compartidas_strings:
                        transicones_compartidas.append(int(transcion_compartida_string))
                else:
                    transicones_compartidas.append(int(plazas_aux)) # El nombre de la plaza_aux es el numero de transicion compartida que esta atada a esta
                
                vector_plazas_necesarias = []
                columnas_abuscar_matriz_relacion = []
                for transicon_compartida in transicones_compartidas:
                    for plaza, valor_plaza in enumerate(matriz_incidencia_transpuesta[transicon_compartida-1]):
                        if valor_plaza < 0:
                            vector_plazas_necesarias.append(plaza)

                    columnas_abuscar_matriz_relacion.append(transiciones_borde.index(transicon_compartida))  # Obtengo la columna que quiero verificar de la matriz de relacion para saber que subred las tienen como borde
                
                for num_subred, fila in enumerate(matriz_relacion):
                    sigo = True
                    if num_subred != indice: # Si esa subred tiene el esa transicion borde y no es la subred que estoy analizando entonces sigo
                        for columna_abuscar_matriz_relacion in columnas_abuscar_matriz_relacion:
                            if fila[columna_abuscar_matriz_relacion] != 1:
                                sigo = False
                                break
                        if sigo and lista_arboles_de_alcanzabilidad[num_subred]["none"]["completo"]:
                            marcado_para_completar, nodo_que_conecta = buscarMarcadoDeseado(lista_arboles_de_alcanzabilidad[num_subred]["none"]["nodos"], vector_plazas_necesarias)
                            if len(marcado_para_completar) > 0:
                                nodo_propio = completarNodo(subred[plazas_aux]["nodos"], caminos_con_inicio_fin_complejo_encontrados[indice], marcado_para_completar[0]) # Por el momento solo voy a conectarlo con uno pero lo mejor seria conectarlo con todos
                                subred[plazas_aux]["conectado"] = True
                                transicion_que_interconecta = []
                                transicion_que_interconecta.append(nodo_que_conecta) #TODO: FUNCIONA PARA CUANDO SOLO SE INTERCONECTA CON 1 T (0_1)
                                transicion_que_interconecta.append(int(plazas_aux))
                                transicion_que_interconecta.append(nodo_propio)
                                print("detecte la conexion: ", transicion_que_interconecta)
                                subred[plazas_aux]["conexiones"].append(transicion_que_interconecta)
                                completeuna = True
    if completeuna:
        procesarSubredRelacionada(indice)
                            

# Recoro todas las subredes y le envio la lista de nodos, lista de plazas con su nombre global incluyendo las auxiliares y marcado inicial global
# for indice, subred in enumerate(lista_arboles_de_alcanzabilidad):
#     completarNodo(subred["none"]["nodos"], caminos_con_inicio_fin_complejo_encontrados[indice], marcado_inicial)
#     subred["none"]["completo"] = True
# # # print(lista_arboles_de_alcanzabilidad[0]["none"]["nodos"])

interelacion_subredes = []

# for indice, subred in enumerate(lista_arboles_de_alcanzabilidad):
#     completarSubred(indice, subred)

completarSubred(0, lista_arboles_de_alcanzabilidad[0])

for i, arboles in enumerate(lista_arboles_de_alcanzabilidad):
    # print(arboles)
    print("a", arboles)
    generate_mincov_json_filled(arboles, i)


print(json.dumps(lista_arboles_de_alcanzabilidad))

arbol_completo = join_tree(lista_arboles_de_alcanzabilidad,N_PLAZAS)
print(arbol_completo)
generate_mincov_json_filled2(arbol_completo)

print("------------------ FINAL ------------------")
print(arbol_completo)