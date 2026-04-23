import os
import requests
from utils.helpers import calcular_distancia
from dotenv import load_dotenv

# Cargo variables del .env (aquí está la API key)
load_dotenv()

# Guardo la API key de AEMET
AEMET_API_KEY = os.getenv("AEMET_API_KEY")


def obtener_clima_por_coordenadas(user_lat, user_lon):
    """
    Devuelve el JSON crudo (RAW) de la estación AEMET más cercana
    a unas coordenadas dadas (latitud y longitud).
    """

    # Compruebo que tengo API key
    if not AEMET_API_KEY:
        raise ValueError("Falta AEMET_API_KEY")

    # AEMET requiere la API key en los headers
    headers = {"api_key": AEMET_API_KEY}

    # Endpoint que devuelve la URL de los datos reales
    url_meta = "https://opendata.aemet.es/opendata/api/observacion/convencional/todas"

    # Primera petición → obtengo metadatos (no los datos directamente)
    res_meta = requests.get(url_meta, headers=headers, timeout=20)
    res_meta.raise_for_status()  # Si falla, lanza error

    # Segunda petición → descargo los datos reales
    datos_url = res_meta.json().get("datos")
    observaciones = requests.get(datos_url, timeout=20).json()

    # Inicializo variables para encontrar la estación más cercana
    estacion_cercana = None
    distancia_minima = float('inf')

    # Recorro todas las estaciones
    for obs in observaciones:
        try:
            # Calculo distancia entre usuario y estación
            dist = calcular_distancia(
                float(user_lat),
                float(user_lon),
                float(obs['lat']),
                float(obs['lon'])
            )

            # Si esta estación está más cerca, la guardo
            if dist < distancia_minima:
                distancia_minima = dist
                estacion_cercana = obs

        # Si hay datos mal formateados, los ignoro
        except (KeyError, ValueError):
            continue

    # Si no he encontrado ninguna estación válida
    if not estacion_cercana:
        raise ValueError("No se encontraron estaciones")

    # Devuelvo el JSON TAL CUAL viene de AEMET (sin tocar)
    return estacion_cercana