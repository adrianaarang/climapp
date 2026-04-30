from flask import Blueprint, request, jsonify
from models.registro_climatico import RegistroClimatico
from repositories.json_repository import JSONRepository
from services.alert_service import AlertService  # Importación desde tu carpeta 'service'
import json

manual_bp = Blueprint('manual', __name__)

# Instancias globales
repo = JSONRepository('data/registros_climaticos.json')
alert_service = AlertService()

@manual_bp.route('/api/registrar', methods=['POST'])
def registrar_datos_manuales():
    """
    Recibe datos JSON, los valida, los guarda y evalúa alertas climáticas.
    """
    try:
        datos = request.get_json()
        if not datos:
            return jsonify({"status": "error", "message": "No se recibieron datos"}), 400

        # 1. Crear el objeto de registro (Persona 2)
        nuevo_registro = RegistroClimatico(
            datos.get("estacion_id"),
            datos.get("fecha"),
            float(datos.get("temperatura", 0)),
            float(datos.get("humedad", 0)),
            float(datos.get("viento", 0)),
            float(datos.get("lluvia", 0))
        )

        # 2. Preparar el diccionario final
        registro_dict = nuevo_registro.to_dict()
        registro_dict["municipio"] = datos.get("municipio", "Desconocido")
        registro_dict["fuente"] = "manual"

        # 3. EVALUAR ALERTAS (Tu AlertService)
        # El controlador envía el registro al motor de alertas antes de confirmar
        lista_alertas = alert_service.evaluar_alertas(registro_dict)

        # 4. Guardar en el JSON de datos
        exito = repo.guardar(registro_dict)

        if exito:
            return jsonify({
                "status": "success",
                "message": "Registro guardado con éxito",
                "alertas": lista_alertas, # Enviamos la lista de strings: ['ROJA', 'VIENTO_FUERTE'...]
                "municipio": registro_dict["municipio"]
            }), 201
        
        return jsonify({"status": "error", "message": "Error al escribir en el repositorio"}), 500

    except Exception as e:
        return jsonify({"status": "error", "message": f"Error interno: {str(e)}"}), 500