from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os

# Importamos los controladores (Blueprints)
from controllers.view_controller import view_bp
from controllers.manual_controller import manual_bp  # <--- ¡Importante: El trabajo de Isabella!

# Importamos los servicios
from services.weather_api_service import obtener_clima_por_coordenadas 
from services.normalizer_service import normalizar_datos_aemet

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "clave_secreta")

# --- REGISTRO DE BLUEPRINTS ---
# Isabella, he registrado aquí tu manual_bp para que todas las rutas 
# de registro de datos queden activas automáticamente.
app.register_blueprint(view_bp)
app.register_blueprint(manual_bp)

@app.route("/api/clima")
def api_clima():
    """
    Orquestador de datos API: Obtiene datos RAW y los normaliza.
    """
    lat = request.args.get('lat')
    lon = request.args.get('lon')

    if not lat or not lon:
        return jsonify({"error": "Faltan las coordenadas GPS (lat/lon)"}), 400

    try:
        # 1. Capa de Servicio: Obtiene el JSON RAW
        raw_data = obtener_clima_por_coordenadas(lat, lon)
        
        # 2. Capa de Normalización: Traduce al estándar de Climapp
        data_normalizada = normalizar_datos_aemet(raw_data)
        
        return jsonify(data_normalizada), 200

    except Exception as e:
        print(f"Error en el endpoint /api/clima: {e}")
        return jsonify({"error": str(e)}), 500

# --- INICIO DE LA APLICACIÓN ---
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)