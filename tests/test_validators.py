import pytest

from utils.validators import (
    comprobar_si_es_numero,
    validar_fecha,
    validar_temperatura,
    validar_humedad,
    validar_viento,
    validar_lluvia,
    validate_weather_data
)


# =====================================================
# FIXTURE: registro climático válido
# =====================================================

@pytest.fixture
def valid_weather_data():
    
    #Datos válidos para probar la función principal validate_weather_data().
    
    return {
        "fecha": "27-04-2026 13:30:00",
        "temperatura": 22.5,
        "humedad": 60,
        "viento": 10.2,
        "lluvia": 0
    }


# =====================================================
# TESTS comprobar_si_es_numero()
# =====================================================

def test_comprobar_si_es_numero_con_numero():
    
    #Si recibe un número, debe devolverlo convertido a float.
    
    assert comprobar_si_es_numero(22, "Temperatura") == 22.0


def test_comprobar_si_es_numero_con_string_numerico():
    
    #Si recibe un string numérico, debe convertirlo a float.
    
    assert comprobar_si_es_numero("22.5", "Temperatura") == 22.5


def test_comprobar_si_es_numero_con_texto():
    
    #Si recibe texto no numérico, debe devolver None.
    
    assert comprobar_si_es_numero("hola", "Temperatura") is None


def test_comprobar_si_es_numero_vacio():
    
    #Si recibe vacío o espacios, debe devolver None.
    
    assert comprobar_si_es_numero("", "Temperatura") is None
    assert comprobar_si_es_numero("   ", "Temperatura") is None


def test_comprobar_si_es_numero_none():
   
    #Si recibe None, debe devolver None.
    
    assert comprobar_si_es_numero(None, "Temperatura") is None


# =====================================================
# TESTS validar_fecha()
# =====================================================

def test_validar_fecha_formato_preferido():
    
    #Formato preferido: día-mes-año con hora completa.
    
    assert validar_fecha("27-04-2026 13:30:00") is True


def test_validar_fecha_con_barras():
   
    #Formato europeo con barras.
   
    assert validar_fecha("27/04/2026 13:30:00") is True


def test_validar_fecha_sin_segundos():
    
    #Formato día-mes-año sin segundos.
    
    assert validar_fecha("27-04-2026 13:30") is True


def test_validar_fecha_formato_html():
    
    #Formato típico de navegador/input datetime-local.
    
    assert validar_fecha("2026-04-27T13:30") is True


def test_validar_fecha_formato_iso_con_segundos():
    
    #Formato año-mes-día con segundos.
    
    assert validar_fecha("2026-04-27 13:30:00") is True


def test_validar_fecha_incorrecta():
    
    #Fecha con formato inválido.
    
    assert validar_fecha("27-04-2026") is False
    assert validar_fecha("fecha incorrecta") is False
    assert validar_fecha("") is False
    assert validar_fecha(None) is False


# =====================================================
# TESTS validar_temperatura()
# =====================================================

def test_validar_temperatura_valida():
    assert validar_temperatura(20) is True
    assert validar_temperatura("22.5") is True


def test_validar_temperatura_limites_validos():
    assert validar_temperatura(-50) is True
    assert validar_temperatura(60) is True


def test_validar_temperatura_invalida():
    assert validar_temperatura(-51) is False
    assert validar_temperatura(61) is False
    assert validar_temperatura("hola") is False
    assert validar_temperatura(None) is False


# =====================================================
# TESTS validar_humedad()
# =====================================================

def test_validar_humedad_valida():
    assert validar_humedad(50) is True
    assert validar_humedad("75") is True


def test_validar_humedad_limites_validos():
    assert validar_humedad(0) is True
    assert validar_humedad(100) is True


def test_validar_humedad_invalida():
    assert validar_humedad(-1) is False
    assert validar_humedad(101) is False
    assert validar_humedad("texto") is False
    assert validar_humedad(None) is False


# =====================================================
# TESTS validar_viento()
# =====================================================

def test_validar_viento_valido():
    assert validar_viento(0) is True
    assert validar_viento(10.5) is True
    assert validar_viento("12") is True


def test_validar_viento_invalido():
    assert validar_viento(-1) is False
    assert validar_viento("mucho") is False
    assert validar_viento(None) is False


# =====================================================
# TESTS validar_lluvia()
# =====================================================

def test_validar_lluvia_valida():
    assert validar_lluvia(0) is True
    assert validar_lluvia(5.4) is True
    assert validar_lluvia("1.2") is True


def test_validar_lluvia_invalida():
    assert validar_lluvia(-0.1) is False
    assert validar_lluvia("llueve") is False
    assert validar_lluvia(None) is False


# =====================================================
# TESTS validate_weather_data()
# =====================================================

def test_validate_weather_data_valido(valid_weather_data):
    
    #Si todos los campos son válidos, debe devolver True.
    
    assert validate_weather_data(valid_weather_data) is True


def test_validate_weather_data_fecha_invalida(valid_weather_data):
    
    #Si la fecha no es válida, debe devolver False.
    
    valid_weather_data["fecha"] = "fecha incorrecta"
    assert validate_weather_data(valid_weather_data) is False


def test_validate_weather_data_temperatura_invalida(valid_weather_data):
    valid_weather_data["temperatura"] = 100
    assert validate_weather_data(valid_weather_data) is False


def test_validate_weather_data_humedad_invalida(valid_weather_data):
    valid_weather_data["humedad"] = 150
    assert validate_weather_data(valid_weather_data) is False


def test_validate_weather_data_viento_invalido(valid_weather_data):
    valid_weather_data["viento"] = -5
    assert validate_weather_data(valid_weather_data) is False


def test_validate_weather_data_lluvia_invalida(valid_weather_data):
    valid_weather_data["lluvia"] = -1
    assert validate_weather_data(valid_weather_data) is False


def test_validate_weather_data_diccionario_vacio():
    
    #Si recibe un diccionario vacío, debe devolver False.
    
    assert validate_weather_data({}) is False


def test_validate_weather_data_none():
    
    #Si recibe None, debe devolver False.
    
    assert validate_weather_data(None) is False


def test_validate_weather_data_no_diccionario():
    
    #  Si recibe algo que no es un diccionario, debe devolver False.
    
    assert validate_weather_data("no soy un diccionario") is False