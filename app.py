from flask import Flask, jsonify, request  # Añadimos request
from dotenv import load_dotenv
import os

from controllers.view_controller import view_bp
# Cambiamos la importación a la nueva función dinámica
from services.weather_api_service import obtener_clima_por_coordenadas 

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "clave_secreta")

app.register_blueprint(view_bp)

@app.route("/api/clima")
def api_clima():
    """
    Ruta dinámica que recibe latitud y longitud desde el frontend
    y devuelve el tiempo de la estación AEMET más cercana.
    """
    # Obtenemos los parámetros enviados por el JS
    lat = request.args.get('lat')
    lon = request.args.get('lon')

    if not lat or not lon:
        return jsonify({"error": "Faltan las coordenadas GPS (lat/lon)"}), 400

    try:
        # Llamamos a la nueva función que calcula la distancia
        data = obtener_clima_por_coordenadas(lat, lon)
        return jsonify(data), 200
    except Exception as e:
        # Si algo falla (ej. AEMET caído), devolvemos el error
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)