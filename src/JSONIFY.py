from flask import Flask, jsonify
from flask_cors import CORS
from SaveData import obtener_ram_global, obtener_ssd, listar_apps_ram, desglosar_almacenamiento_ssd

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
#  Devuelve: lista de procesos ordenados por consumo (pid, app, ram_usada_mb, porcentaje)
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
#  Devuelve: sistema_gb, aplicaciones_gb, multimedia_gb
# ------------------------------------------------------------
@app.route('/api/ssd/desglose')
def ssd_desglose():
    return jsonify(desglosar_almacenamiento_ssd())


# ------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
