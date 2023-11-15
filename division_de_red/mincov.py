from typing import List

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
