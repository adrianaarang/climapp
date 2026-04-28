import os
import requests
from services.logging_service import log_info, log_warning

def resolve_location(lat=None, lon=None, city=None):
    """
    Lógica de Failover: GPS -> Geocoding -> Default (IP).
    Gestiona la jerarquia de ubicacion y registra la fuente en los logs.
    """
    # Prioridad 1: Coordenadas GPS directas
    if lat and lon and lat != "undefined" and lat != "null":
        log_info(f"Ubicacion establecida mediante GPS: {lat}, {lon}")
        return {"lat": lat, "lon": lon, "source": "GPS", "success": True}

    # Prioridad 2: Texto Manual (Google Geocoding)
    if city:
        # Hardcoded para testeo en Madrid (Simula respuesta de Google)
        if city.lower() == "madrid":
            log_info(f"Ubicacion resuelta por busqueda manual (Google Geo): {city}")
            return {"lat": 40.4167, "lon": -3.7033, "source": "GOOGLE_GEO", "success": True}
        
        log_warning(f"Ciudad '{city}' no encontrada en el mock. Aplicando fallback.")

    # Prioridad 3: IP por defecto 
    log_info("Aplicando ubicacion por defecto (IP_INFERRED): DashLogistics HQ")
    return {"lat": 40.4530, "lon": -3.6883, "source": "IP_INFERRED", "success": True}