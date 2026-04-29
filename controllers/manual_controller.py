from flask import Blueprint, request, jsonify
from models.registro_climatico import RegistroClimatico
from utils.validators import validate_weather_data
from repositories.json_repository import append
from services.logging_service import log_info, log_error # Importamos los logs de Elena

manual_bp = Blueprint('manual', __name__)

@manual_bp.route('/api/registrar', methods=['POST'])
def registrar_datos_manuales():
    """
    Controlador mejorado para DashLogistics. 
    Integra validación, persistencia en JSON y logging profesional.
    """
    datos_recibidos = request.get_json()

    if not datos_recibidos:
        log_error("API Manual: Intento de registro sin datos.")
        return jsonify({"error": "No se recibió el paquete de datos"}), 400

    datos_para_validar = {
        "municipio":     datos_recibidos.get("municipio"),
        "estacion_id":   datos_recibidos.get("estacion_id"),
        "fecha":         datos_recibidos.get("fecha"),
        "temperatura":   datos_recibidos.get("temperatura"),
        "humedad":       datos_recibidos.get("humedad"),
        "viento":        datos_recibidos.get("viento"),
        "lluvia":        datos_recibidos.get("lluvia")
    }
    
    estacion = datos_para_validar["estacion_id"] or "DESCONOCIDA"

    # Log de intento de entrada
    log_info(f"API Manual: Iniciando proceso de registro para estación {estacion}")

    if validate_weather_data(datos_para_validar):
        try:
            # Creamos el objeto RegistroClimatico con los tipos de datos correctos
            nuevo_registro = RegistroClimatico(
                estacion,
                datos_para_validar["fecha"],
                float(datos_para_validar["temperatura"]),
                float(datos_para_validar["humedad"]),
                float(datos_para_validar["viento"]),
                float(datos_para_validar["lluvia"])
            )
            
            # Ejecutamos el guardado
            resultado = append(nuevo_registro.to_dict())
            
            # Verificamos si el diccionario de respuesta indica éxito
            if resultado.get("success"):
                log_info(f"API Manual: Registro guardado con éxito para {estacion}")
                return jsonify({
                    "status": "success",
                    "message": "✔ Registro guardado correctamente",
                    "data": nuevo_registro.to_dict()
                }), 201
            else:
                error_repo = resultado.get("error", "Error interno en el repositorio")
                log_error(f"API Manual: Fallo al escribir en disco: {error_repo}")
                return jsonify({"error": f"Error al guardar: {error_repo}"}), 500
            
        except Exception as e:
            log_error(f"API Manual: Error crítico de procesamiento: {str(e)}")
            return jsonify({"error": f"Error interno: {str(e)}"}), 400
    else:
        log_error(f"API Manual: Fallo de validación en datos recibidos: {datos_para_validar}")
        return jsonify({
            "status": "error", 
            "message": "❌ Los datos no son válidos. Revisa el formato de fecha (DD-MM-AAAA HH:MM) y los rangos numéricos."
        }), 400