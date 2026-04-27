import datetime

def comprobar_si_es_numero(valor, nombre):
    """
    Isabella, aquí he corregido el error de retorno que teníamos.
    Ahora la función devuelve el float(valor) correctamente para que 
    el resto de funciones puedan comparar rangos numéricos.
    """
    try:
        if valor is None or str(valor).strip() == "":
            return None
        return float(valor)
    except (ValueError, TypeError):
        return None

def validar_fecha(fecha_texto):
    """
    He priorizado el formato Día-Mes-Año.
    He añadido un bucle que prueba varios formatos (europeo y el estándar de HTML)
    para que la app sea más flexible y no de error si el usuario cambia el formato.
    """
    if not fecha_texto: return False
    
    # Limpiamos la 'T' que suelen incluir los navegadores en los inputs de fecha
    fecha_texto = fecha_texto.replace('T', ' ')
    
    formatos_a_probar = [
        "%d-%m-%Y %H:%M:%S", # Formato preferido: 27-04-2026 13:30:00
        "%d/%m/%Y %H:%M:%S",
        "%d-%m-%Y %H:%M",
        "%Y-%m-%d %H:%M",    # Formato nativo de navegadores
        "%Y-%m-%d %H:%M:%S"
    ]
    
    for formato in formatos_a_probar:
        try:
            datetime.datetime.strptime(fecha_texto, formato)
            return True
        except ValueError:
            continue
    return False

def validar_temperatura(valor):
    """Valida rango físico lógico entre -50 y 60 grados."""
    t = comprobar_si_es_numero(valor, "Temperatura")
    return t is not None and -50 <= t <= 60

def validar_humedad(valor):
    """Asegura que el porcentaje esté en el rango 0-100."""
    h = comprobar_si_es_numero(valor, "Humedad")
    return h is not None and 0 <= h <= 100

def validar_viento(valor):
    """Valida que la velocidad no sea negativa."""
    v = comprobar_si_es_numero(valor, "Viento")
    return v is not None and v >= 0

def validar_lluvia(valor):
    """Valida que la precipitación no sea negativa."""
    ll = comprobar_si_es_numero(valor, "Lluvia")
    return ll is not None and ll >= 0

# --- FUNCIÓN DE INTEGRACIÓN (CRÍTICA PARA EL CONTROLADOR) ---
def validate_weather_data(data):
    """
    Isabella, esta es la función 'maestra' que invoca el controlador.
    Usa tu lógica de all() para asegurar que TODOS los campos sean válidos
    antes de crear el objeto RegistroClimatico.
    """
    if not data or not isinstance(data, dict):
        return False
        
    return all([
        validar_fecha(data.get("fecha")),
        validar_temperatura(data.get("temperatura")),
        validar_humedad(data.get("humedad")),
        validar_viento(data.get("viento")),
        validar_lluvia(data.get("lluvia"))
    ])