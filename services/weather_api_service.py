import os
import requests
import math
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

AEMET_API_KEY = os.getenv("AEMET_API_KEY")

def calcular_distancia(lat1, lon1, lat2, lon2):
    """Calcula la distancia en km entre dos puntos (Haversine)."""
    rad = math.pi / 180
    dlat = (lat2 - lat1) * rad
    dlon = (lon2 - lon1) * rad
    a = math.sin(dlat/2)**2 + math.cos(lat1*rad) * math.cos(lat2*rad) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return 6371 * c

def obtener_clima_por_coordenadas(user_lat, user_lon):
    if not AEMET_API_KEY:
        raise ValueError("Falta AEMET_API_KEY")

    headers = {"api_key": AEMET_API_KEY}
    
    # 1) Obtener URL de datos
    url = "https://opendata.aemet.es/opendata/api/observacion/convencional/todas"
    response = requests.get(url, headers=headers, timeout=20)
    response.raise_for_status()
    
    datos_url = response.json().get("datos")
    observaciones = requests.get(datos_url, timeout=20).json()

    # 2) Encontrar la estación más cercana
    estacion_cercana = None
    distancia_minima = float('inf')

    for obs in observaciones:
        try:
            est_lat = float(obs['lat'])
            est_lon = float(obs['lon'])
            dist = calcular_distancia(float(user_lat), float(user_lon), est_lat, est_lon)
            if dist < distancia_minima:
                distancia_minima = dist
                estacion_cercana = obs
        except (KeyError, ValueError):
            continue

    if not estacion_cercana:
        raise ValueError("No se encontraron estaciones")

    # 3) Lógica de Día/Noche basada en TU hora real
    hora_actual = datetime.now().hour
    # Es noche si son más de las 21:00 o antes de las 07:00
    es_noche = hora_actual >= 21 or hora_actual <= 7

    return {
        "temperatura": estacion_cercana.get("ta", 0),
        "humedad": estacion_cercana.get("hr", 0),
        "viento": estacion_cercana.get("vv", 0),
        "lluvia": estacion_cercana.get("prec", 0),
        "fecha": estacion_cercana.get("fint", ""),
        "estacion": estacion_cercana.get("ubi", "Desconocida"),
        "ciudad": estacion_cercana.get("ubi", "Tu Zona"),
        "fuente": "AEMET",
        "es_noche": es_noche,
        "hora_display": datetime.now().strftime("%H:%M")
        
    }