import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("AEMET_API_KEY")

URL = "https://opendata.aemet.es/opendata/api/valores/climatologicos/inventarioestaciones/todasestaciones"

HEADERS = {
    "api_key": API_KEY
}

def generar_estaciones_madrid():
    # Paso 1: llamar a AEMET
    response = requests.get(URL, headers=HEADERS)
    data = response.json()

    # Paso 2: coger URL de datos reales
    datos_url = data["datos"]

    estaciones = requests.get(datos_url).json()

    # Paso 3: filtrar Madrid
    madrid = [
        {
            "indicativo": e["indicativo"],
            "nombre": e["nombre"],
            "latitud": e["latitud"],
            "longitud": e["longitud"],
            "altitud": e["altitud"]
        }
        for e in estaciones if e["provincia"] == "MADRID"
    ]

    # Paso 4: guardar JSON
    os.makedirs("config", exist_ok=True)

    with open("config/estaciones_madrid.json", "w", encoding="utf-8") as f:
        json.dump(madrid, f, indent=2, ensure_ascii=False)

    print(f"✅ {len(madrid)} estaciones guardadas en estaciones_madrid.json")


if __name__ == "__main__":
    generar_estaciones_madrid()

    # esto es para que nos haga el json de las estacioens de madrid y las guarde. Nos faltaría la KEY API DE LA AEMET
