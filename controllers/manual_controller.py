from utils.validators import validators_weather_data
from models.registro_climatico import RegistroClimatico

def capturar_datos_manuales():
    print("--- Captura de Datos Climáticos ---")

    # 1. Recoger datos del usuario
    estacion = input("ID de la Estación: ")
    fecha = input("Fecha (AAAA-MM-DD HH:MM:SS): ")
    temp = input("Temperatura (ºC): ")
    hum = input("Humedad (%): ")
    viento = input("Viento (Km/H): ")
    lluvia = input("Lluvia (mm): ")

    # 2. Creación de diccionario para validar
    datos = {
        "fecha"         :    fecha,
        "temperatura"   :    temp,
        "humedad"       :    hum,
        "viento"        :    viento,
        "lluvia"        :    lluvia
    }

    # 3. Uso de nueva función de integración
    if validators_weather_data(datos):
        # Si es True se crea el objeto con el modelo creado
        nuevo_registro = RegistroClimatico(estacion, fecha, temp, hum, viento, lluvia)
        print("✔ Registro creado con éxito")
        return nuevo_registro.to_dict()
    else:
        print("❌ Error: Los datos no son válidos. Revisa rangos y formatos.")
        return None  