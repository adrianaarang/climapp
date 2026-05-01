from flask import Blueprint, jsonify, request
from services.weather_api_service import obtener_clima_por_coordenadas
from services.normalizer_service import normalizar_datos_aemet
# Importamos la función de tu archivo repositories/json_repository.py
from repositories.json_repository import guardar_registro 

api_bp = Blueprint('api', __name__)

@api_bp.route("/api/clima")
def api_clima():
    lat = request.args.get("lat")
    lon = request.args.get("lon")

    if not lat or not lon:
        return jsonify({"error": "Faltan coordenadas"}), 400

    try:
        raw_data = obtener_clima_por_coordenadas(lat, lon)
        data = normalizar_datos_aemet(raw_data)

        # Mantenemos tu lógica de seguridad para la ciudad
        if 'ciudad' not in data:
            data['ciudad'] = data.get('municipio', 'Ubicación Detectada')

        # --- EL PASO QUE FALTA: GUARDAR ---
        # Añadimos la fuente para que tus filtros (manual/aemet) funcionen después
        data['fuente'] = 'aemet' 
        
        # Llamamos a tu repositorio JSON
        guardar_registro(data) 

        return jsonify(data), 200

    except Exception as e:
        print(f"Error en api_controller: {e}")
        return jsonify({
            "error": str(e),
            "temperatura": 0,
            "ciudad": "Error de conexión",
            "humedad": 0
        }), 500