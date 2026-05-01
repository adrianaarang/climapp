from flask import Blueprint, jsonify, request
from services.weather_api_service import obtener_clima_por_coordenadas
from services.normalizer_service import normalizar_datos_aemet

api_bp = Blueprint('api', __name__)

@api_bp.route("/api/clima")
def api_clima():
    lat = request.args.get("lat")
    lon = request.args.get("lon")

    if not lat or not lon:
        return jsonify({"error": "Faltan coordenadas"}), 400

    try:
        # 1. Obtenemos datos de AEMET
        raw_data = obtener_clima_por_coordenadas(lat, lon)
        
        # 2. Normalizamos (Asegúrate de que este servicio devuelva la clave 'ciudad')
        data = normalizar_datos_aemet(raw_data)

        # 3. DOBLE SEGURIDAD: Si el normalizador no pone 'ciudad', lo ponemos nosotros
        # Esto evita el "undefined" en el frontend
        if 'ciudad' not in data:
            data['ciudad'] = data.get('municipio', 'Ubicación Detectada')

        return jsonify(data), 200

    except Exception as e:
        print(f"Error en api_controller: {e}")
        # Enviamos un objeto con estructura mínima para que el JS no rompa
        return jsonify({
            "error": str(e),
            "temperatura": 0,
            "ciudad": "Error de conexión",
            "humedad": 0
        }), 500