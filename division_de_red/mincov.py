from typing import List
from itertools import compress, product
import re
import copy



def set_to_string(items):
    string_set = '-'.join(list([str(num) for num in items]))
    return string_set

def list_to_string(lista: List[int]) -> str:
    return "[" + ", ".join([str(elem) for elem in lista]) + " ]"
  
def combinations(items):
    return ( set(compress(items,mask)) for mask in product(*[[0,1]]*len(items)) )

def stateToList(state: str) -> List[int]:
    a = state.split(" ")[:-1]
    a[0] = a[0][1:]
    a = [int(x) for x in a]
    return a

def clasificar_plazas(matriz_incidencia: List[List[int]]) -> List[List[int]]:
    plazas_simples = []
    plazas_complejas = []
    plazas_dos_entradas_una_salida = []
    plazas_dos_salidas_una_entrada = []
    
    for i in range(len(matriz_incidencia)):
        tipos_entradas = {1: 0, -1: 0}
        for j in range(len(matriz_incidencia[0])):
            if matriz_incidencia[i][j] > 0:
                tipos_entradas[1] += 1
            elif matriz_incidencia[i][j] < 0:
                tipos_entradas[-1] += 1

        if not (tipos_entradas[1] > 1 or tipos_entradas[-1] > 1):
            plazas_simples.append(i + 1)  # Plazas con como máximo 1 entrada y 1 salida
        else:
            if tipos_entradas[1] == 2 and tipos_entradas[-1] <= 1:
                plazas_dos_entradas_una_salida.append(i + 1)  # Plazas con 2 entradas y 1 salida máximo
            elif tipos_entradas[1] <= 1 and tipos_entradas[-1] == 2:
                plazas_dos_salidas_una_entrada.append(i + 1)  # Plazas con 1 entrada y 2 salidas máximo
            else:
                plazas_complejas.append(i + 1)
    
    # Nota: plazas_complejas_total debe calcularse dentro de la función para mantener la pureza.
    plazas_complejas_total = plazas_complejas + plazas_dos_entradas_una_salida + plazas_dos_salidas_una_entrada

    return [plazas_simples, plazas_complejas, plazas_dos_entradas_una_salida, plazas_dos_salidas_una_entrada, plazas_complejas_total]

def clasificar_transiciones(matriz_incidencia, plazas_complejas, plazas_dos_entradas_una_salida, plazas_dos_salidas_una_entrada):
    transiciones_indeseadas = set()
    transiciones_indeseadas_totales = set()
    transiciones_plazas_dos_entradas_una_salida = []
    transiciones_plazas_dos_salidas_una_entrada = []
    dict_plazas_dos_entradas_una_salida = {}
    dict_plazas_dos_salidas_una_entrada = {}

    for j in range(len(matriz_incidencia[0])):
        for i in plazas_complejas:
            if matriz_incidencia[i - 1][j] != 0:
                transiciones_indeseadas.add(j + 1)
                transiciones_indeseadas_totales.add(j + 1)

        for i in plazas_dos_entradas_una_salida:
            if matriz_incidencia[i - 1][j] != 0:
                transiciones_indeseadas_totales.add(j + 1)
                transiciones_plazas_dos_entradas_una_salida.append(j + 1)
                dict_plazas_dos_entradas_una_salida[j + 1] = i

        for i in plazas_dos_salidas_una_entrada:
            if matriz_incidencia[i - 1][j] != 0:
                transiciones_indeseadas_totales.add(j + 1)
                transiciones_plazas_dos_salidas_una_entrada.append(j + 1)
                dict_plazas_dos_salidas_una_entrada[j + 1] = i

    return transiciones_indeseadas, transiciones_indeseadas_totales, \
        transiciones_plazas_dos_entradas_una_salida, \
        transiciones_plazas_dos_salidas_una_entrada, \
        dict_plazas_dos_entradas_una_salida, \
        dict_plazas_dos_salidas_una_entrada

def try_add_to_train_2i1o_1i2o(
    t,
    res_con_plazas_especiales,
    res_transiciones_usadas_con_plazas_especiales,
    transiciones_plazas_dos_entradas_una_salida,
    dict_plazas_dos_entradas_una_salida,
    plazas_dos_entradas_una_salida,
    transiciones_plazas_dos_salidas_una_entrada,
    dict_plazas_dos_salidas_una_entrada,
    plazas_dos_salidas_una_entrada,
    transiciones_borde,
    matriz_incidencia):
    if (t+1 in transiciones_plazas_dos_entradas_una_salida 
            and t+1 in dict_plazas_dos_entradas_una_salida
            and dict_plazas_dos_entradas_una_salida[t+1] in plazas_dos_entradas_una_salida
            and matriz_incidencia[dict_plazas_dos_entradas_una_salida[t+1] - 1][t] > 0): # Si es de entrada
        plaza_dos_entradas_una_salida = dict_plazas_dos_entradas_una_salida[t+1]
        transiciones_borde.remove(t+1)
        plaza_index = plazas_dos_entradas_una_salida.index(plaza_dos_entradas_una_salida)
        plazas_dos_entradas_una_salida.pop(plaza_index)
        res_con_plazas_especiales.append(plaza_dos_entradas_una_salida)
        for tt in range(len(matriz_incidencia[0])):
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
        for tt in range(len(matriz_incidencia[0])):
            if(tt != t and matriz_incidencia[plaza_dos_salidas_una_entrada - 1][tt] != 0):
                res_transiciones_usadas_con_plazas_especiales.add(tt+1)
        del plaza_dos_salidas_una_entrada



def join_tree(arbol_de_alcanzabilidad):
    nodos = {}
    conexiones = []
    for subred_padre in arbol_de_alcanzabilidad:
        for subred_hija in subred_padre:
            if subred_padre[subred_hija]["completo"]:
                print("COMPLETO: ", subred_padre[subred_hija]["nodos"])
                nodos = nodos | subred_padre[subred_hija]["nodos"]
                conexiones += subred_padre[subred_hija]["conexiones"]
    return {"nodos" : nodos, "conexiones" : conexiones}


import json

def generate_mincov_json_input_general(matriz, marcado_inicial) -> str:
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

def generate_mincov_json_input(i, matriz, plazas_temp_con_mark, caminos_con_inicio_fin_complejo_encontrados, marcado_inicial) -> str:
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
            if plaza_a_verificar < 0:  # significa que es una aux
                if plaza_a_verificar * -1 in plazas_temp_con_mark:
                    plaza = {
                        "index": j,
                        "type": "discrete",
                        "initial_marking": 1,
                    }
                else:
                    plaza = {
                        "index": j,
                        "type": "discrete",
                        "initial_marking": 0,
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

def getArbolFromSalida(s: str, numero_sub_red: int, index_nodos: int, is_none: bool, transiciones_de_caminos_con_inicio_fin_complejo_encontrados):
    with open(f"salida/{s}") as salida:
        salida_json = json.load(salida)
        array_nodos = {}  # n1 = [0, 0, 1, 0] va a ser {1: [0, 0, 1, 0]}
        array_conexiones = []  # n1 -> t5 -> n2 va a ser [1, 5, 2]
        conexiones_agregadas = set()

        for nodes in salida_json["nodes"]:
            n = int(nodes["id"][1:])
            if n != 1 or not is_none:
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
                temp.append(transiciones_de_caminos_con_inicio_fin_complejo_encontrados[numero_sub_red][int(re.search(r".*T(\d+)", n).groups()[0]) - 1])
                temp.append(nodo_to)
                array_conexiones.append(temp)
        new_index_nodos = index_nodos + len(array_nodos) + 1
        if is_none and len(array_nodos) == 1:
            new_index_nodos -= 1
        print("len", len(array_nodos))
        print("new_index_nodos", new_index_nodos)
        print("proximo", new_index_nodos + len(array_nodos))
        return {"nodos": array_nodos, "conexiones": array_conexiones, "completo": False}, new_index_nodos - 1

def completar_nodo(lista_nodos_subred, lista_orden_plazas_subred, marcado_inicial, N_PLAZAS, plaza_con_marcado_deseado):
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
                    nodo[i] = marcado_inicial[i]
                else:
                    nodo.append(marcado_inicial[i])

    for p in plaza_con_marcado_deseado: #TODO: Revisar porque esta mal
        marcado_inicial[p] += 1

    for nodo in lista_nodos_subred:
        if lista_nodos_subred[nodo] == marcado_inicial:
            return nodo
    print("No encontré ningún cambio")
    return -1  # También se podría devolver un booleano que indique que no se encontró nada

def buscar_marcado_deseado(lista_nodos_subred, plaza_con_marcado_deseado_propias, plaza_con_marcado_deseado_no_propias):
    lista_nodos_subred_cpy = copy.deepcopy(lista_nodos_subred)
    lista_marcados_posibles = []
    nodo_que_conecta = -1
    for key, nodo in lista_nodos_subred.items():
        conecta = True
        for p in plaza_con_marcado_deseado_propias:
            if nodo[p] < 1:
                conecta = False
                break
        for p in plaza_con_marcado_deseado_no_propias:
            if nodo[p] < 1:
                conecta = False
                break
            else:
                lista_nodos_subred_cpy[key][p] -= 1
        if conecta:
            nodo_que_conecta = key
            lista_marcados_posibles.append(lista_nodos_subred_cpy[key])
    return lista_marcados_posibles, nodo_que_conecta

def procesar_subred_relacionada(indice, matriz_relacion, lista_arboles_de_alcanzabilidad, matriz_incidencia_transpuesta, transiciones_borde, caminos_con_inicio_fin_complejo_encontrados, marcado_inicial, N_PLAZAS):
    for indice_mr, valor in enumerate(matriz_relacion[indice]):
        if valor == 1:
            for indice_red, red in enumerate(matriz_relacion):
                if indice_red != indice and red[indice_mr] == 1:
                    completar_subred(indice_red, lista_arboles_de_alcanzabilidad[indice_red], matriz_incidencia_transpuesta, matriz_relacion, lista_arboles_de_alcanzabilidad, transiciones_borde, caminos_con_inicio_fin_complejo_encontrados, marcado_inicial, N_PLAZAS)
                    break  # Detiene el bucle una vez que se completa la subred


def completar_subred(indice, subred, matriz_incidencia_transpuesta, matriz_relacion, lista_arboles_de_alcanzabilidad, transiciones_borde, caminos_con_inicio_fin_complejo_encontrados, marcado_inicial, N_PLAZAS):
    completeuna = False
    for plazas_aux in subred:
        if subred[plazas_aux]["completo"] == False: 
            if "none" in plazas_aux:
                completar_nodo(subred[plazas_aux]["nodos"], caminos_con_inicio_fin_complejo_encontrados[indice], marcado_inicial, N_PLAZAS, [])
                completeuna = True
                subred["none"]["completo"] = True
            else:
                transicones_compartidas = []
                if "-" in plazas_aux: 
                    transiciones_compartidas_strings = plazas_aux.split("-")
                    for transcion_compartida_string in transiciones_compartidas_strings:
                        transicones_compartidas.append(int(transcion_compartida_string))
                else:
                    transicones_compartidas.append(int(plazas_aux)) 
                
                vector_plazas_necesarias_propias = [] #de la red a completar
                vector_plazas_necesarias_no_propias = []
                columnas_abuscar_matriz_relacion = []
                for transicon_compartida in transicones_compartidas:
                    for plaza, valor_plaza in enumerate(matriz_incidencia_transpuesta[transicon_compartida-1]):
                        # if valor_plaza < 0 and not (plaza+1 in caminos_con_inicio_fin_complejo_encontrados[indice]):
                        if valor_plaza < 0:
                            if plaza+1 in caminos_con_inicio_fin_complejo_encontrados[indice]:
                                vector_plazas_necesarias_propias.append(plaza)
                            else:
                                vector_plazas_necesarias_no_propias.append(plaza)

                    columnas_abuscar_matriz_relacion.append(transiciones_borde.index(transicon_compartida))
                
                for num_subred, fila in enumerate(matriz_relacion):
                    sigo = True
                    for columna_abuscar_matriz_relacion in columnas_abuscar_matriz_relacion:
                        if fila[columna_abuscar_matriz_relacion] != 1: # Esto pasa si la subred no tiene todas las transiciones para activar el estado incial de la subred que intento completar
                            sigo = False
                            break
                    if sigo:
                        for arbol in lista_arboles_de_alcanzabilidad[num_subred].values():
                            if arbol["completo"]:
                                marcado_para_completar, nodo_que_conecta = buscar_marcado_deseado(arbol["nodos"], vector_plazas_necesarias_propias, vector_plazas_necesarias_no_propias)
                                if len(marcado_para_completar) > 0:
                                    nodo_propio = completar_nodo(subred[plazas_aux]["nodos"], caminos_con_inicio_fin_complejo_encontrados[indice], marcado_para_completar[0], N_PLAZAS, vector_plazas_necesarias_proias)
                                    if nodo_propio != -1:
                                        subred[plazas_aux]["completo"] = True
                                        transicion_que_interconecta = []
                                        transicion_que_interconecta.append(nodo_que_conecta) 
                                        transicion_que_interconecta.append(int(plazas_aux))
                                        transicion_que_interconecta.append(nodo_propio)
                                        print("detecte la conexion: ", transicion_que_interconecta)
                                        subred[plazas_aux]["conexiones"].append(transicion_que_interconecta)
                                        completeuna = True
                                        break 
    if completeuna:
        procesar_subred_relacionada(indice, matriz_relacion, lista_arboles_de_alcanzabilidad, matriz_incidencia_transpuesta, transiciones_borde, caminos_con_inicio_fin_complejo_encontrados, marcado_inicial, N_PLAZAS)
