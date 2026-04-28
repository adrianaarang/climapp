def validate_weather_schema(data):
    """
    Asegura que el diccionario tenga los tipos correctos.
    Si algo falla, devuelve un esquema seguro (Null Object Pattern).
    """
    try:
        return {
            "temperatura": float(data.get("temp", 0.0)),
            "humedad": float(data.get("hum", 0.0)),
            "viento": float(data.get("wind", 0.0)),
            "valido": True
        }
    except (TypeError, ValueError):
        return {
            "temperatura": 0.0,
            "humedad": 0.0,
            "viento": 0.0,
            "valido": False
        }