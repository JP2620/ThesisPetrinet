
# Python program to read
# json file
  
  
import json
from typing import List
from os import listdir
from os.path import isfile, join
from itertools import compress, product
import numpy as np

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

def generate_mincov_json_input_general(matriz) -> None:
    with open("./salida/matriz_incidencia_general.json", "w") as f:
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

def generate_mincov_json_input (i, matriz, plazas_temp_con_mark) -> None:
    with open("./salida/matriz_incidencia_" + str(i) + "_" + set_to_string(plazas_temp_con_mark) + ".json", "w") as f:
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

# Opening JSON file
f = open('matriz.json')
  
# returns JSON object as 
# a dictionary
data = json.load(f)
matriz_incidencia = data["Incidencia"]
marcado_inicial = data["Marcado"]

N_PLAZAS = len(matriz_incidencia)
N_TRANSICIONES = len(matriz_incidencia[0])

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
            print("Deberia agregar la plaza", p, "en el arreglo", caminos_con_inicio_fin_complejo_encontrados[t_conjunto], "y", temp, "en ", transiciones_de_caminos_con_inicio_fin_complejo_encontrados[t_conjunto])
            caminos_con_inicio_fin_complejo_encontrados[t_conjunto].append(p)
            for t_faltantes in temp:
                transiciones_de_caminos_con_inicio_fin_complejo_encontrados[t_conjunto].add(t_faltantes)
            for t_no_faltantes in temp2:
                transiciones_borde.remove(t_no_faltantes)
                for p_conectados in range(N_PLAZAS):
                    if(matriz_incidencia[p_conectados-1][t_no_faltantes-1] != 0 and not p_conectados+1 in caminos_con_inicio_fin_complejo_encontrados[t_conjunto]):
                        transiciones_borde.add(t_no_faltantes) # Si hay alguna plaza que no forme parte del subconujunto agrego la transicion como borde
            print("Deberia agregar la plaza", p, "en el arreglo", caminos_con_inicio_fin_complejo_encontrados[t_conjunto], "y", temp, "en ", transiciones_de_caminos_con_inicio_fin_complejo_encontrados[t_conjunto])
            break
    if not encontro:
        caminos_con_inicio_fin_complejo_encontrados.append([p])
        transiciones_de_caminos_con_inicio_fin_complejo_encontrados.append(transiciones_conectadas)

            
# Calculo Matriz Relacion:
matriz_relacion = []
transiciones_con_plazas_aux = []
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
    print("")

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




for abc in matriz_incidencia_caminos_complejos:
    print("\n\n",abc)

for i, matriz in enumerate(matriz_incidencia_caminos_complejos):
    generate_mincov_json_input(i,matriz, set())
    for plazas_temp_con_mark in combinations(transiciones_con_plazas_aux[i]):
        if len(plazas_temp_con_mark) > 0:
            set_to_string(plazas_temp_con_mark)
            generate_mincov_json_input(i,matriz, plazas_temp_con_mark)
generate_mincov_json_input_general(matriz_incidencia)








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
        return salida_json

PREFIX = "mincov_out_"
salidasMinCov = [f for f in listdir("salida") if f.find(PREFIX) != -1]
lista_arboles_de_alcanzabilidad = []
for i, subred in enumerate(caminos_con_inicio_fin_complejo_encontrados):
    salidas_de_la_subred = [s for s in salidasMinCov if s.startswith(f"{PREFIX}{i}")]
    if len(salidas_de_la_subred) > 0:
        lista_arboles_de_alcanzabilidad.append([])
        arboles = lista_arboles_de_alcanzabilidad[i]
        for s in salidas_de_la_subred:
            arboles.append(getArbolFromSalida(s))

print(lista_arboles_de_alcanzabilidad)







