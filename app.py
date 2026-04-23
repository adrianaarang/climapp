from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os

from controllers.view_controller import view_bp
# Importamos tanto el servicio de API como el normalizador
from services.weather_api_service import obtener_clima_por_coordenadas 
from services.normalizer_service import normalizar_datos_aemet

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "clave_secreta")

app.register_blueprint(view_bp)

@app.route("/api/clima")
def api_clima():
    """
    Ruta que orquestra la obtención de datos RAW y su posterior
    normalización antes de enviarlos al frontend.
    """
    lat = request.args.get('lat')
    lon = request.args.get('lon')

    if not lat or not lon:
        return jsonify({"error": "Faltan las coordenadas GPS (lat/lon)"}), 400

    try:
        # 1. Capa de Servicio: Obtiene el JSON RAW de la estación más cercana
        # (Aquí weather_api_service ya no calcula es_noche ni formatea nada)
        raw_data = obtener_clima_por_coordenadas(lat, lon)
        
        # 2. Capa de Normalización: Traduce el RAW de AEMET a nuestro estándar
        # (Aquí es donde se calcula el es_noche, fecha_display, etc.)
        data_normalizada = normalizar_datos_aemet(raw_data)
        
        return jsonify(data_normalizada), 200

    except Exception as e:
        # Registramos el error en consola para debug y lo enviamos al front
        print(f"Error en el endpoint /api/clima: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)