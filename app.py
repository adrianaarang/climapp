from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os

# Importamos controladores
from controllers.view_controller import view_bp
from controllers.manual_controller import manual_bp 

# Importamos servicios
from services.weather_api_service import obtener_clima_por_coordenadas 
from services.normalizer_service import normalizar_datos_aemet
from services.location_resolver_service import resolve_location
from services.logging_service import log_info, log_error 
from repositories.json_repository import append           

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "clave_secreta")

# Registro de Blueprints para vistas y registro manual
app.register_blueprint(view_bp)
app.register_blueprint(manual_bp)

@app.route("/api/clima")
def api_clima():
    """
    Gateway inteligente: Resuelve ubicacion, obtiene datos y los persiste 
    en el repositorio local.
    """
    # 1. Resolucion de Ubicacion (Failover Protocol)
    location_data = resolve_location(
        lat=request.args.get('lat'),
        lon=request.args.get('lon'),
        city=request.args.get('ciudad')
    )

    if not location_data["success"]:
        log_warning("No se pudo determinar la ubicacion en /api/clima")
        return jsonify({
            "status": "warning",
            "message": "No se pudo determinar la ubicación. Use búsqueda manual."
        }), 200

    try:
        lat, lon = location_data["lat"], location_data["lon"]
        fuente = location_data["source"]

        # 2. Obtencion de datos climáticos
        raw_data = obtener_clima_por_coordenadas(lat, lon)
        
        # 3. Normalizacion y Generacion de ID 
        data_normalizada = normalizar_datos_aemet(raw_data, fuente_ubicacion=fuente)
        
        # 4. Persistencia automatica (Integracion con JSON Repository)
        if data_normalizada:
            resultado = append(data_normalizada)
            if resultado["success"]:
                log_info(f"Dato persistido correctamente: {data_normalizada['id']}")
            else:
                log_error(f"Error al guardar en repositorio: {resultado['message']}")
        
        return jsonify(data_normalizada), 200

    except Exception as e:
        log_error(f"Error critico en el endpoint /api/clima: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500

if __name__ == "__main__":
    # Servidor en modo desarrollo
    app.run(debug=True, host="0.0.0.0", port=5000)