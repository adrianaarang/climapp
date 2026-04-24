import os
import requests
from utils.helpers import calcular_distancia
from dotenv import load_dotenv

# Cargamos variables de entorno (.env) ahí tenemos la key api que os pasé
load_dotenv()
AEMET_API_KEY = os.getenv("AEMET_API_KEY")

def obtener_clima_por_coordenadas(user_lat, user_lon):
    """
    Localiza la estación de AEMET más cercana y devuelve sus datos 
    en formato RAW (crudo) para que el normalizador los procese.
    """

    if not AEMET_API_KEY:
        raise ValueError("No se encontró la AEMET_API_KEY en las variables de entorno.")

    headers = {
        "api_key": AEMET_API_KEY,
        "cache-control": "no-cache"
    }

    # 1. Obtener la URL de los datos (AEMET OpenData funciona así)
    url_meta = "https://opendata.aemet.es/opendata/api/observacion/convencional/todas"
    
    try:
        res_meta = requests.get(url_meta, headers=headers, timeout=20)
        res_meta.raise_for_status()
        
        datos_url = res_meta.json().get("datos")
        if not datos_url:
            raise ValueError("La API de AEMET no devolvió una URL de datos válida.")

        # 2. Descargar las observaciones reales
        res_datos = requests.get(datos_url, timeout=20)
        res_datos.raise_for_status()
        observaciones = res_datos.json()

    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Error de conexión con AEMET: {e}")

    # 3. Encontrar la estación más cercana
    estacion_cercana = None
    distancia_minima = float('inf')

    for obs in observaciones:
        try:
            # Extraemos coordenadas de la estación actual
            obs_lat = float(obs['lat'])
            obs_lon = float(obs['lon'])

            dist = calcular_distancia(
                float(user_lat), 
                float(user_lon), 
                obs_lat, 
                obs_lon
            )

            if dist < distancia_minima:
                distancia_minima = dist
                estacion_cercana = obs

        except (KeyError, ValueError, TypeError):
            # Saltamos estaciones con datos incompletos
            continue

    if not estacion_cercana:
        raise ValueError("No se encontraron estaciones meteorológicas válidas.")

    # IMPORTANTE: Devolvemos el diccionario original (RAW)
    # No renombramos 'ta' a 'temperatura', eso lo hará el normalizador.
    return estacion_cercana

            # 24/04 A la espera de intregar con Isabela