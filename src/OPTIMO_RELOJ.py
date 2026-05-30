import random

def generar_cadena_referencia(longitud, max_paginas):
    return [random.randint(0, max_paginas) for _ in range(longitud)]

def algoritmo_optimo(cadena_referencia, num_marcos):
    marcos = []
    fallos_pagina = 0
    historial = []
    
    for i, pagina in enumerate(cadena_referencia):
        paso_actual = {
            "pagina_solicitada": pagina,
            "accion": "",
            "marcos_resultantes": []
        }
        
        if pagina not in marcos:
            fallos_pagina += 1
            paso_actual["accion"] = "Fallo"
            
            if len(marcos) < num_marcos:
                marcos.append(pagina)
            else:
                indice_mas_lejano = -1
                indice_reemplazo = -1
                
                for j, pag_marco in enumerate(marcos):
                    if pag_marco not in cadena_referencia[i+1:]:
                        indice_reemplazo = j
                        break
                    else:
                        proximo_uso = cadena_referencia[i+1:].index(pag_marco)
                        if proximo_uso > indice_mas_lejano:
                            indice_mas_lejano = proximo_uso
                            indice_reemplazo = j
                            
                marcos[indice_reemplazo] = pagina
        else:
            paso_actual["accion"] = "Acierto"
            
        paso_actual["marcos_resultantes"] = list(marcos)
        historial.append(paso_actual)
        
    return {
        "metodo": "Optimo",
        "cadena_referencia": cadena_referencia,
        "total_fallos": fallos_pagina,
        "detalles_paso_a_paso": historial
    }

def algoritmo_reloj(cadena_referencia, num_marcos):
    marcos = []
    bits_uso = []
    puntero = 0
    fallos_pagina = 0
    historial = []
    
    for pagina in cadena_referencia:
        paso_actual = {
            "pagina_solicitada": pagina,
            "accion": "",
            "marcos_resultantes": [],
            "bits_uso_resultantes": [],
            "posicion_puntero": 0
        }
        
        if pagina in marcos:
            paso_actual["accion"] = "Acierto"
            indice = marcos.index(pagina)
            bits_uso[indice] = 1
        else:
            fallos_pagina += 1
            paso_actual["accion"] = "Fallo"
            
            if len(marcos) < num_marcos:
                marcos.append(pagina)
                bits_uso.append(1)
            else:
                while True:
                    if bits_uso[puntero] == 0:
                        marcos[puntero] = pagina
                        bits_uso[puntero] = 1
                        puntero = (puntero + 1) % num_marcos
                        break
                    else:
                        bits_uso[puntero] = 0
                        puntero = (puntero + 1) % num_marcos
                        
        paso_actual["marcos_resultantes"] = list(marcos)
        paso_actual["bits_uso_resultantes"] = list(bits_uso)
        paso_actual["posicion_puntero"] = puntero
        
        historial.append(paso_actual)
        
    return {
        "metodo": "Reloj",
        "cadena_referencia": cadena_referencia,
        "total_fallos": fallos_pagina,
        "detalles_paso_a_paso": historial
    }