
# Python program to read
# json file
  
  
import json
from typing import List
from os import listdir, system
from os.path import isfile, join
from itertools import compress, product
import numpy as np
import re
import copy

PATH_MINCOV = "./salida/PetrinetSE-original"

""" Entra set() sale <elemento1>-<elemento1><elemento1>-<elemento1> """
def set_to_string(items):
    string_set = '-'.join(list([str(num) for num in items]))
    return string_set
  
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

# print("Marcado Inicial:",marcado_inicial)
# print("\nCamino con matriz_relacionentradas y salidas:")
# print("Plazas:",caminos_con_inicio_fin_complejo_encontrados)
# print("Transiciones:", transiciones_de_caminos_con_inicio_fin_complejo_encontrados)
# print("M Incidencia:",matriz_incidencia_caminos_complejos)
# # print("Tamaño matriz relacion", len(transiciones_borde), "x", len(caminos_con_inicio_fin_complejo_encontrados))
# print("Transiciones borde", transiciones_borde)
# print("Matriz relacion", matriz_relacion)
# print("Plazas aux", transiciones_con_plazas_aux)

# Closing file
f.close()




"""
matriz_incidencia_... son entradas del algoritmo de gabi
- Ejecutar algoritmo de gabi con cada una de esas entradas
- Renombrar salidas del algoritmo de gabi con el patrón mincov_out_...etc
"""

mincov_inputs = []
for i, matriz in enumerate(matriz_incidencia_caminos_complejos):
    generate_mincov_json_input(i,matriz, set())
    for plazas_temp_con_mark in combinations(transiciones_con_plazas_aux[i]):
        if len(plazas_temp_con_mark) > 0:
            set_to_string(plazas_temp_con_mark)
            mincov_input_filename = generate_mincov_json_input(i,matriz, plazas_temp_con_mark)
            mincov_inputs.append(mincov_input_filename)
mincov_inputs.append(generate_mincov_json_input_general(matriz_incidencia))



for mincov_input in mincov_inputs:
    system(f"{PATH_MINCOV} -a {mincov_input}")
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

def getArbolFromSalida(s: str):
    with open(f"salida/{s}") as salida:
        salida_json = json.load(salida)
        array_nodos = {} # n1 = [0,0,1,0] va a ser {1: [0,0,1,0]}
        array_conexiones = [] # n1 -> t5 -> n2 va a ser [1,5,2]
        conexiones_agregadas = set()

        for nodes in salida_json["nodes"]:
            n = int(nodes["id"][1:])
            state = stateToList(nodes["state"])
            array_nodos[n] = state

        for conexiones in salida_json["edges"]:
            n = conexiones["path"]
            if n not in conexiones_agregadas:
                conexiones_agregadas.add(n)
                temp = []
                temp.append(int(conexiones["from"][1:]))
                temp.append(int(re.search(r".*T(\d+)", n).groups()[0]))
                temp.append(int(conexiones["to"][1:]))
                array_conexiones.append(temp)

        return {"nodos" : array_nodos, "conexiones": array_conexiones}

PREFIX = "mincov_out_"
salidasMinCov = [f for f in sorted(listdir("salida")) if f.find(PREFIX) != -1]
lista_arboles_de_alcanzabilidad = []

for i, subred in enumerate(caminos_con_inicio_fin_complejo_encontrados):
    salidas_de_la_subred = [s for s in salidasMinCov if s.startswith(f"{PREFIX}{i}")]
    if len(salidas_de_la_subred) > 0:
        lista_arboles_de_alcanzabilidad.append({})
        arboles = lista_arboles_de_alcanzabilidad[i]

        for s in salidas_de_la_subred:
            plazas_aux_con_marcadoinicial = s[s.index(str(i))+2:].split(".")[0]
            identificador_posibilidad = plazas_aux_con_marcadoinicial if plazas_aux_con_marcadoinicial != "" else "none"
            arboles[identificador_posibilidad] = getArbolFromSalida(s)

# print("aca empieza")
# print(lista_arboles_de_alcanzabilidad)

def completarNodo(lista_nodos_subred, lista_orden_plazas_subred, marcado_incial):
    lista_nodos_subred_cpy = copy.deepcopy(lista_nodos_subred)
    for i in range(N_PLAZAS):
        if i+1 in lista_orden_plazas_subred:
            posicion = lista_orden_plazas_subred.index(i+1)
            for nodos in lista_nodos_subred:
                nodo = lista_nodos_subred[nodos]
                nodo_cpy = lista_nodos_subred_cpy[nodos]
                if i < len(nodo):
                    nodo[i] = nodo_cpy[posicion]
                else:
                    nodo.append(nodo_cpy[posicion])
        else:
            for nodos in lista_nodos_subred:
                nodo = lista_nodos_subred[nodos]
                if i < len(nodo):
                    nodo[i] = marcado_incial[i]
                else:
                    nodo.append(marcado_incial[i])

def buscarMarcadoDeseado(lista_nodos_subred, plaza_con_marcado_deseada): # Solo busca el primer marcarcado
    lista_nodos_subred_cpy = copy.deepcopy(lista_nodos_subred)
    lista_marcados_posibles = []
    for key, nodo in lista_nodos_subred.items():
        conecta = True
        for p in plaza_con_marcado_deseada:
            if nodo[p] < 1:
                conecta = False
                break
            else:
                lista_nodos_subred_cpy[key][p] -= 1
            # ANTES TIENE QUE ELIMINAR UN MARCADO DE ESTA PLAZA
        if conecta: 
            lista_marcados_posibles.append(lista_nodos_subred_cpy[key])
    return lista_marcados_posibles

# # print(lista_arboles_de_alcanzabilidad[0]["none"]["nodos"])
for indice, subred in enumerate(lista_arboles_de_alcanzabilidad):
    completarNodo(subred["none"]["nodos"], caminos_con_inicio_fin_complejo_encontrados[indice], marcado_inicial)
# # print(lista_arboles_de_alcanzabilidad[0]["none"]["nodos"])


for indice, subred in enumerate(lista_arboles_de_alcanzabilidad):
    for plazas_aux in subred:
        if plazas_aux != "none": # Las none ya las analice arriba
            transicon_compartida = int(plazas_aux) # El nombre de la plaza_aux es el numero de transicion compartida que esta atada a esta
            
            vector_plazas_necesarias = []
            for plaza, valor_plaza in enumerate(matriz_incidencia_transpuesta[transicon_compartida-1]):
                if valor_plaza < 0:
                    vector_plazas_necesarias.append(plaza)

            columna_abuscar_matriz_relacion = transiciones_borde.index(transicon_compartida) # Obtengo la columna que quiero verificar de la matriz de relacion para saber que subred las tienen como borde
            for num_subred, fila in enumerate(matriz_relacion):
                if fila[columna_abuscar_matriz_relacion] == 1 and num_subred != indice: # Si esa subred tiene el esa transicion borde y no es la subred que estoy analizando entonces sigo
                    marcado_para_completar = buscarMarcadoDeseado(lista_arboles_de_alcanzabilidad[num_subred]["none"]["nodos"], vector_plazas_necesarias)
                    if len(marcado_para_completar) > 0:
                        completarNodo(subred[plazas_aux]["nodos"], caminos_con_inicio_fin_complejo_encontrados[indice], marcado_para_completar[0]) # Por el momento solo voy a conectarlo con uno pero lo mejor seria conectarlo con todos
