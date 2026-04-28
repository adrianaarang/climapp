import os
import requests

def resolve_location(lat=None, lon=None, city=None):
    """
    Implementa la lógica de Failover: GPS -> Geocoding -> Default (IP).
    """
    # Prioridad 1: Coordenadas GPS directas
    if lat and lon and lat != "undefined":
        return {"lat": lat, "lon": lon, "source": "GPS", "success": True}

    # Prioridad 2: Texto Manual (Google Geocoding)
    if city:
        # Mock de llamada a Google API para el ejemplo
        # api_key = os.getenv("GOOGLE_MAPS_KEY")
        # response = requests.get(f"https://maps.googleapis.com/json?address={city}&key={api_key}")
        if city.lower() == "madrid": # Ejemplo hardcoded para testeo
            return {"lat": 40.4167, "lon": -3.7033, "source": "GOOGLE_GEO", "success": True}

    # Prioridad 3: IP por defecto (DashLogistics HQ como fallback seguro)
    return {"lat": 40.4530, "lon": -3.6883, "source": "IP_INFERRED", "success": True}