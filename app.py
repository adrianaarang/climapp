from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os

# Importamos los controladores (Blueprints)
from controllers.view_controller import view_bp
from controllers.manual_controller import manual_bp  # <--- ¡Importante: El trabajo de Isabella!

# Importamos los servicios
from services.weather_api_service import obtener_clima_por_coordenadas 
from services.normalizer_service import normalizar_datos_aemet
from services.location_resolver_service import resolve_location

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
    Intelligent Gateway: Resuelve la ubicación por jerarquía (GPS > Manual > IP)
    y orquesta la obtención de datos climáticos.
    """
    # 1. Resolución de Ubicación (Failover Protocol)
    location_data = resolve_location(
        lat=request.args.get('lat'),
        lon=request.args.get('lon'),
        city=request.args.get('ciudad')
    )

    if not location_data["success"]:
        return jsonify({
            "status": "warning",
            "message": "No se pudo determinar la ubicación. Use búsqueda manual."
        }), 200

    try:
        lat, lon = location_data["lat"], location_data["lon"]
        fuente = location_data["source"]

        # 2. Obtención de datos con AEMET (o fallback a Google Weather)
        raw_data = obtener_clima_por_coordenadas(lat, lon)
        
        # 3. Normalización y Validación (Integrando el trabajo de Elena)
        data_normalizada = normalizar_datos_aemet(raw_data, fuente_ubicacion=fuente)
        
        return jsonify(data_normalizada), 200

    except Exception as e:
        print(f"Error en el endpoint /api/clima: {e}")
        return jsonify({"error": str(e)}), 500

# --- INICIO DE LA APLICACIÓN ---
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)