from flask import Flask, jsonify, request, render_template
from dotenv import load_dotenv
import os

# Importamos controladores
from controllers.view_controller import view_bp
from controllers.manual_controller import manual_bp 

# Importamos servicios
from services.weather_api_service import obtener_clima_por_coordenadas 
from services.normalizer_service import normalizar_datos_aemet
from services.location_resolver_service import resolve_location
from services.logging_service import log_info, log_error, log_warning
from repositories.json_repository import append            

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "clave_secreta")

# Registro de Blueprints
app.register_blueprint(view_bp)
app.register_blueprint(manual_bp)

@app.route("/api/clima")
def api_clima():
    """
    Gateway inteligente: Resuelve ubicación, obtiene datos y los persiste.
    Diseñado para el JS de Adriana.
    """
    # 1. Extracción de parámetros de la URL
    lat_req = request.args.get('lat')
    lon_req = request.args.get('lon')
    ciudad_req = request.args.get('ciudad')

    # Fallback preventivo: Si llega todo vacío, forzamos Madrid para evitar el "Cargando..."
    if not lat_req and not lon_req and not ciudad_req:
        ciudad_req = "Madrid"

    # 2. Resolución de Ubicación (Llamada al servicio corregido)
    location_data = resolve_location(
        lat=lat_req,
        lon=lon_req,
        city=ciudad_req
    )

    # Verificación de seguridad
    if not location_data.get("success"):
        log_warning("Fallo en resolución de ubicación. Usando datos de emergencia.")
        return jsonify({
            "status": "warning",
            "message": "Ubicación no encontrada.",
            "municipio": "Madrid"
        }), 200

    try:
        lat_res = location_data["lat"]
        lon_res = location_data["lon"]
        fuente = location_data["source"]

        # 3. Obtención de datos reales de la API
        raw_data = obtener_clima_por_coordenadas(lat_res, lon_res)
        
        # 4. Normalización (Crucial para que el JS vea 'temperatura', 'humedad', etc.)
        data_normalizada = normalizar_datos_aemet(raw_data, fuente_ubicacion=fuente)
        
        # 5. Persistencia en el Repositorio JSON
        if data_normalizada:
            # El repositorio devuelve un booleano (True/False)
            exito_guardado = append(data_normalizada)
            
            if exito_guardado:
                log_info(f"Registro guardado: {data_normalizada.get('municipio')} ({fuente})")
            else:
                log_error("Error al persistir datos en registros_climaticos.json")
        
        # 6. Respuesta final al Frontend (JS de Adriana)
        return jsonify(data_normalizada), 200

    except Exception as e:
        log_error(f"Error crítico en el Gateway /api/clima: {e}")
        return jsonify({
            "error": "Error interno del servidor", 
            "details": str(e)
        }), 500

if __name__ == "__main__":
    # Host 0.0.0.0 para que sea accesible desde otros dispositivos en la red
    app.run(debug=True, host="0.0.0.0", port=5000)