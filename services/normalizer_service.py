import logging
# 1. Importamos tu servicio de alertas
from services.alert_service import AlertService

# Instanciamos el servicio para tenerlo listo
alert_service = AlertService()

def normalizar_datos_aemet(data, fuente_ubicacion="AEMET"):
    """
    Transforma los datos crudos de AEMET en un formato estándar 
    e integra el sistema de alertas de Juan, incluyendo la trazabilidad de la fuente.
    """
    try:
        if not data:
            return {"error": "No hay datos disponibles"}

        # Si es una lista, tomamos el último registro (el más reciente)
        latest = data[-1] if isinstance(data, list) else data
        
        # 2. Creamos el diccionario base
        datos_normalizados = {
            "estacion": latest.get("ubi", "Desconocida"),
            "fecha": latest.get("fint", "N/A"),
            "temperatura": float(latest.get("ta", 0)) if latest.get("ta") else 0,
            "humedad": float(latest.get("hr", 0)) if latest.get("hr") else 0,
            "viento": float(latest.get("vv", 0)) if latest.get("vv") else 0,
            "presion": float(latest.get("pres", 0)) if latest.get("pres") else 0,
            "lluvia": float(latest.get("prec", 0)) if latest.get("prec") else 0,
            # --- CAMBIO AQUÍ: Inyectamos la fuente que viene del Resolver ---
            "fuente": fuente_ubicacion 
        }

        # 3. Usamos tu AlertService para generar las etiquetas
        datos_normalizados["alertas"] = alert_service.evaluar_alertas(datos_normalizados)

        return datos_normalizados

    except Exception as e:
        logging.error(f"Error en normalización: {e}")
        return {"error": "Error al procesar los datos"}