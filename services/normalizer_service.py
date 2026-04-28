import uuid
from services.alert_service import AlertService
from services.logging_service import log_error

# Modulo de alertas y logs de la aplicacion
alert_service = AlertService()

def normalizar_datos_aemet(data, fuente_ubicacion="AEMET"):
    """
    Estandariza los datos de AEMET, genera identificadores unicos 
    y asegura compatibilidad con el sistema de persistencia y alertas.
    """
    try:
        if not data:
            return None

        latest = data[-1] if isinstance(data, list) else data
        
        # Generacion de diccionario compatible
        datos_normalizados = {
            "id": str(uuid.uuid4()),
            "municipio": latest.get("ubi", "Desconocida"),
            "estacion": latest.get("ubi", "Desconocida"),
            "fecha": latest.get("fint", "N/A"),
            "temperatura": float(latest.get("ta", 0)) if latest.get("ta") else 0,
            "humedad": float(latest.get("hr", 0)) if latest.get("hr") else 0,
            "viento": float(latest.get("vv", 0)) if latest.get("vv") else 0,
            "presion": float(latest.get("pres", 0)) if latest.get("pres") else 0,
            "lluvia": float(latest.get("prec", 0)) if latest.get("prec") else 0,
            "fuente": fuente_ubicacion 
        }

        # Procesamiento de reglas de negocio para alertas
        datos_normalizados["alertas"] = alert_service.evaluar_alertas(datos_normalizados)

        return datos_normalizados

    except Exception as e:
        log_error(f"Error en normalizacion de datos: {e}")
        return None