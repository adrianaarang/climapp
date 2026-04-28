from flask import Blueprint, request, jsonify
from models.registro_climatico import RegistroClimatico
from utils.validators import validate_weather_data
from repositories.json_repository import append # <-- Usamos la función nueva

manual_bp = Blueprint('manual', __name__)

@manual_bp.route('/api/registrar', methods=['POST'])
def registrar_datos_manuales():
    """
    Controlador con logs de depuración para identificar fallos de validación.
    """
    datos_recibidos = request.get_json()

    if not datos_recibidos:
        return jsonify({"error": "No se recibió el paquete de datos"}), 400

    datos_para_validar = {
        "fecha":         datos_recibidos.get("fecha"),
        "temperatura":   datos_recibidos.get("temperatura"),
        "humedad":       datos_recibidos.get("humedad"),
        "viento":        datos_recibidos.get("viento"),
        "lluvia":        datos_recibidos.get("lluvia")
    }
    
    estacion = datos_recibidos.get("estacion_id")

    # LOG PARA CONSOLA: Así veremos qué llega exactamente
    print(f"\n--- INTENTO DE REGISTRO ---")
    print(f"Datos recibidos: {datos_para_validar}")

    if validate_weather_data(datos_para_validar):
        try:
            nuevo_registro = RegistroClimatico(
                estacion, 
                datos_para_validar["fecha"], 
                float(datos_para_validar["temperatura"]), 
                float(datos_para_validar["humedad"]), 
                float(datos_para_validar["viento"]), 
                float(datos_para_validar["lluvia"])
            )
            
            exito_guardado = append(nuevo_registro.to_dict())
            
            if exito_guardado:
                print("✔ ÉXITO: Guardado en JSON")
                return jsonify({
                    "status": "success",
                    "message": "✔ Registro guardado correctamente",
                    "data": nuevo_registro.to_dict()
                }), 201
            else:
                print("❌ ERROR: Fallo al escribir en disco")
                return jsonify({"error": "No se pudo escribir en el archivo"}), 500
            
        except Exception as e:
            print(f"❌ ERROR DE PROCESAMIENTO: {e}")
            return jsonify({"error": str(e)}), 400
    else:
        # Si entra aquí, uno de los validadores de utils/validators.py ha devuelto False
        print("❌ FALLO DE VALIDACIÓN: Revisa los formatos en utils/validators.py")
        return jsonify({
            "status": "error", 
            "message": "❌ Los datos no son válidos. Revisa especialmente el formato de fecha (DD-MM-AAAA HH:MM)."
        }), 400