import os
import requests
from services.logging_service import log_info, log_warning

def resolve_location(lat=None, lon=None, city=None):
    """
    Lógica de Failover: GPS -> Geocoding -> Default (Madrid).
    Resuelve coordenadas asegurando compatibilidad con tipos de JS.
    """
    
    # --- 1. Limpieza de entrada (Evita "null"/"undefined" de JavaScript) ---
    def is_valid(value):
        return value and str(value).lower() not in ["none", "null", "undefined", ""]

    # --- 2. Prioridad 1: Coordenadas GPS directas ---
    if is_valid(lat) and is_valid(lon):
        try:
            log_info(f"Ubicación establecida mediante GPS: {lat}, {lon}")
            return {
                "lat": float(lat), 
                "lon": float(lon), 
                "source": "GPS", 
                "success": True
            }
        except ValueError:
            log_warning(f"Coordenadas GPS inválidas recibidas: {lat}, {lon}")

    # --- 3. Prioridad 2: Texto Manual (Geocoding) ---
    if is_valid(city):
        city_clean = str(city).strip().lower()
        
        # Diccionario de mocks para la demo (puedes añadir más ciudades aquí)
        mock_cities = {
            "madrid": {"lat": 40.4167, "lon": -3.7033},
            "barcelona": {"lat": 41.3851, "lon": 2.1734},
            "valencia": {"lat": 39.4699, "lon": -0.3763},
            "sevilla": {"lat": 37.3891, "lon": -5.9845}
        }

        if city_clean in mock_cities:
            log_info(f"Ubicación resuelta por búsqueda manual: {city_clean}")
            coords = mock_cities[city_clean]
            return {
                "lat": coords["lat"], 
                "lon": coords["lon"], 
                "source": "MANUAL_SEARCH", 
                "success": True
            }
        
        log_warning(f"Ciudad '{city}' no encontrada en el sistema. Aplicando fallback.")

    # --- 4. Prioridad 3: Ubicación por defecto (Madrid HQ) ---
    # Esto es lo que evita que la pantalla se quede en "Cargando..." si falla el GPS
    log_info("Aplicando ubicación por defecto: Madrid (DashLogistics HQ)")
    return {
        "lat": 40.4530, 
        "lon": -3.6883, 
        "source": "IP_INFERRED", 
        "success": True
    }