# Importación de la lógica de validación integral y el modelo de datos.
from utils.validators import validate_weather_data
from models.registro_climatico import RegistroClimatico

def capturar_datos_manuales():
    """
    Gestiona el flujo de entrada de datos por consola, coordiona la validación
    y retorna la representación serializada del registro.
    """
    print("\n--- Captura de Datos Climáticos ---")

    # 1. Recolección de entrada (Se reciben inicialmente como strings).
    estacion = input("ID de la Estación: ")
    fecha = input("Fecha (AAAA-MM-DD HH:MM:SS): ")
    temp = input("Temperatura (ºC): ")
    hum = input("Humedad (%): ")
    viento = input("Viento (Km/H): ")
    lluvia = input("Lluvia (mm): ")

    # 2. Estructuración de datos para el proceso de validación.
    datos = {
        "fecha"         :    fecha,
        "temperatura"   :    temp,
        "humedad"       :    hum,
        "viento"        :    viento,
        "lluvia"        :    lluvia
    }

    # 3. Validación de integridad y rangos lógicos.
    if validate_weather_data(datos):
        # Si la validación es exitosa, se instancia el modelo convirtiendo las
        # métricas a float para asegurar la precisión númerica.
        nuevo_registro = RegistroClimatico(
            estacion, 
            fecha, 
            float(temp), 
            float(hum), 
            float(viento), 
            float(lluvia)
            )
        print("✔ Registro creado con éxito")
        # Se retorna el diccionario listo para la persistencia (JSON) o envío a UI.
        return nuevo_registro.to_dict()
    else:
        # Notificación de error en caso de formatos incorrectos o valores fuera de rango.
        print("❌ Error: Los datos no son válidos. Revisa rangos y formatos.")
        return None  