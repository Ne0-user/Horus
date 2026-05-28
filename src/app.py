from flask import Flask, jsonify
from flask_cors import CORS
from SaveData import obtener_ram_global, obtener_ssd

app = Flask(__name__)
CORS(app)

# ------------------------------------------------------------
#  ENDPOINT 1: RAM global
# ------------------------------------------------------------
@app.route('/api/ram')
def ram():
    return jsonify(obtener_ram_global())

# ------------------------------------------------------------
#  ENDPOINT 2: SSD
# ------------------------------------------------------------
@app.route('/api/ssd')
def ssd():
    return jsonify(obtener_ssd())

# ------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
