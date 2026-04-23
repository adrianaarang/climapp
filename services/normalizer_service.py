import locale
from datetime import datetime

# Intento poner el idioma en español para fechas (lunes, martes, etc.)
try:
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')  # Linux / Mac
except:
    try:
        locale.setlocale(locale.LC_TIME, 'spanish')  # Windows
    except:
        locale.setlocale(locale.LC_TIME, '')  # Fallback (idioma del sistema)


def normalizar_datos_aemet(raw_data):
    """
    Convierte el JSON RAW de AEMET al formato estándar de mi app (ClimApp)
    """

    # Cojo la fecha y hora actual del sistema
    ahora = datetime.now()

    return {
        # Temperatura (ta = temperatura en AEMET)
        "temperatura": raw_data.get("ta", 0),

        # Humedad relativa (hr = humedad)
        "humedad": raw_data.get("hr", 0),

        # Velocidad del viento (vv)
        "viento": raw_data.get("vv", 0),

        # Precipitación (prec)
        "lluvia": raw_data.get("prec", 0),

        # Nombre de la estación
        "estacion": raw_data.get("ubi", "Desconocida"),

        # Ciudad (de momento uso lo mismo que estación)
        "ciudad": raw_data.get("ubi", "Tu Zona"),

        # Detecto si es de noche (para UI: luna/sol)
        "es_noche": ahora.hour >= 21 or ahora.hour <= 7,

        # Fecha bonita tipo: "Lunes, 22 de abril"
        "fecha_display": ahora.strftime("%A, %d de %B").capitalize(),

        # Hora tipo: "14:35"
        "hora_display": ahora.strftime("%H:%M"),

        "fuente": "AEMET"
    }