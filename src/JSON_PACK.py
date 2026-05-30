from flask import Flask, jsonify, request
from flask_cors import CORS
from SaveData import obtener_ram_global, obtener_ssd, listar_apps_ram, desglosar_almacenamiento_ssd
from LRU_FIFO import LRU, FIFO
from OPTIMO_RELOJ import algoritmo_optimo, algoritmo_reloj, generar_cadena_referencia

app = Flask(__name__)
CORS(app)

# ------------------------------------------------------------
#  ENDPOINT 1: RAM global
#  Devuelve: total_gb, usado_gb, porcentaje_uso, cache_gb
# ------------------------------------------------------------
@app.route('/api/ram')
def ram():
    return jsonify(obtener_ram_global())


# ------------------------------------------------------------
#  ENDPOINT 2: Aplicaciones y cuánta RAM consumen
#  Devuelve: lista de procesos ordenados por consumo
# ------------------------------------------------------------
@app.route('/api/ram/apps')
def ram_apps():
    return jsonify(listar_apps_ram())


# ------------------------------------------------------------
#  ENDPOINT 3: SSD - uso actual
#  Devuelve: total_gb, usado_gb, libre_gb, porcentaje_uso
# ------------------------------------------------------------
@app.route('/api/ssd')
def ssd():
    return jsonify(obtener_ssd())


# ------------------------------------------------------------
#  ENDPOINT 4: SSD - desglose por categoría
#  ADVERTENCIA: esta función es lenta, puede tardar varios minutos
#  No llamar en intervalos automáticos, solo bajo demanda
#  Devuelve: sistema_gb, aplicaciones_gb, multimedia_gb
# ------------------------------------------------------------
@app.route('/api/ssd/desglose')
def ssd_desglose():
    return jsonify(desglosar_almacenamiento_ssd())


# ------------------------------------------------------------
#  ENDPOINT 5: Algoritmo LRU (Sofía)
#  Parámetros opcionales: n (longitud cadena), p (num marcos)
#  Ejemplo: /api/paginacion/lru?n=10&p=4
#  Devuelve: metodo, cadena, fallos, hits, porcentaje, nivel_fallos
# ------------------------------------------------------------
@app.route('/api/paginacion/lru')
def paginacion_lru():
    n = int(request.args.get('n', 10))
    p = int(request.args.get('p', 4))
    resultado = LRU(n, p)
    return jsonify(resultado.send())


# ------------------------------------------------------------
#  ENDPOINT 6: Algoritmo FIFO (Sofía)
#  Parámetros opcionales: n (longitud cadena), p (num marcos)
#  Ejemplo: /api/paginacion/fifo?n=10&p=4
#  Devuelve: metodo, cadena, fallos, hits, porcentaje, nivel_fallos
# ------------------------------------------------------------
@app.route('/api/paginacion/fifo')
def paginacion_fifo():
    n = int(request.args.get('n', 10))
    p = int(request.args.get('p', 4))
    resultado = FIFO(n, p)
    return jsonify(resultado.send())


# ------------------------------------------------------------
#  ENDPOINT 7: Algoritmo Óptimo (Adal)
#  Parámetros opcionales: marcos, longitud, max_paginas
#  Ejemplo: /api/paginacion/optimo?marcos=3&longitud=10&max_paginas=5
#  Devuelve: metodo, cadena_referencia, total_fallos, detalles_paso_a_paso
# ------------------------------------------------------------
@app.route('/api/paginacion/optimo')
def paginacion_optimo():
    marcos    = int(request.args.get('marcos', 3))
    longitud  = int(request.args.get('longitud', 10))
    max_pags  = int(request.args.get('max_paginas', 5))
    cadena    = generar_cadena_referencia(longitud, max_pags)
    return jsonify(algoritmo_optimo(cadena, marcos))


# ------------------------------------------------------------
#  ENDPOINT 8: Algoritmo Reloj (Adal)
#  Parámetros opcionales: marcos, longitud, max_paginas
#  Ejemplo: /api/paginacion/reloj?marcos=3&longitud=10&max_paginas=5
#  Devuelve: metodo, cadena_referencia, total_fallos, detalles_paso_a_paso
# ------------------------------------------------------------
@app.route('/api/paginacion/reloj')
def paginacion_reloj():
    marcos    = int(request.args.get('marcos', 3))
    longitud  = int(request.args.get('longitud', 10))
    max_pags  = int(request.args.get('max_paginas', 5))
    cadena    = generar_cadena_referencia(longitud, max_pags)
    return jsonify(algoritmo_reloj(cadena, marcos))


# ------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
