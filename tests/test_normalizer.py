import pytest

# Importamos la función que queremos probar.
# Esta función está en services/normalizer_service.py
from services.normalizer_service import normalizar_datos_aemet


# =====================================================
# FIXTURE: datos AEMET simulados
# =====================================================

@pytest.fixture
def sample_aemet_data():
    """
    Esta fixture prepara datos falsos como si vinieran de AEMET.

    Importante:
    - No estamos llamando a la API real.
    - Solo creamos una lista con un diccionario de prueba.
    - Así el test es rápido, seguro y controlado.
    """
    return [
        {
            "ubi": "Madrid-Retiro",              # Nombre de la estación
            "fint": "2026-04-27 13:00:00",      # Fecha/hora del dato
            "ta": "22.5",                       # Temperatura como string
            "hr": "60",                         # Humedad como string
            "vv": "10",                         # Viento como string
            "pres": "1013",                     # Presión como string
            "prec": "0.5"                       # Lluvia como string
        }
    ]


# =====================================================
# TEST 1: normalización correcta
# =====================================================

def test_normalizar_datos_aemet_correcto(monkeypatch, sample_aemet_data):
    """
    Este test comprueba el caso feliz:
    cuando AEMET devuelve datos correctos y la función los normaliza bien.
    """

    # La función normalizar_datos_aemet llama internamente a:
    # alert_service.evaluar_alertas(...)
    #
    # Como este test es del normalizador, NO queremos depender
    # de la lógica real de alertas.
    #
    # Por eso creamos una función falsa que siempre devuelve
    # una alerta controlada.
    def fake_alertas(data):
        return ["alerta_test"]

    # Con monkeypatch sustituimos temporalmente la función real
    # evaluar_alertas por nuestra función falsa fake_alertas.
    #
    # Solo afecta durante este test.
    monkeypatch.setattr(
        "services.normalizer_service.alert_service.evaluar_alertas",
        fake_alertas
    )

    # Ejecutamos la función que queremos probar usando los datos falsos.
    result = normalizar_datos_aemet(sample_aemet_data)

    # Comprobamos que los campos se han renombrado correctamente.
    assert result["estacion"] == "Madrid-Retiro"
    assert result["fecha"] == "2026-04-27 13:00:00"

    # Comprobamos que los valores numéricos se han convertido a float.
    assert result["temperatura"] == 22.5
    assert result["humedad"] == 60.0
    assert result["viento"] == 10.0
    assert result["presion"] == 1013.0
    assert result["lluvia"] == 0.5

    # Comprobamos que también se añade el campo alertas.
    # Como hemos usado fake_alertas, esperamos exactamente esta lista.
    assert result["alertas"] == ["alerta_test"]


# =====================================================
# TEST 2: entrada como diccionario
# =====================================================

def test_normalizar_datos_aemet_dict(monkeypatch):
    """
    La función admite dos tipos de entrada:
    - una lista de registros
    - un único diccionario

    Este test comprueba que también funciona si recibe directamente un diccionario.
    """

    # Creamos un dato falso en formato diccionario.
    data = {
        "ubi": "Madrid",
        "fint": "2026-04-27 13:00:00",
        "ta": "20",
        "hr": "50",
        "vv": "5",
        "pres": "1000",
        "prec": "0"
    }

    # Sustituimos evaluar_alertas por una función sencilla que devuelve lista vacía.
    # En este test no nos interesa probar alertas.
    monkeypatch.setattr(
        "services.normalizer_service.alert_service.evaluar_alertas",
        lambda x: []
    )

    # Ejecutamos la función.
    result = normalizar_datos_aemet(data)

    # Comprobamos que toma bien los datos del diccionario.
    assert result["estacion"] == "Madrid"
    assert result["temperatura"] == 20.0
    assert result["humedad"] == 50.0
    assert result["viento"] == 5.0
    assert result["presion"] == 1000.0
    assert result["lluvia"] == 0.0
    assert result["alertas"] == []


# =====================================================
# TEST 3: lista vacía
# =====================================================

def test_normalizar_datos_aemet_lista_vacia():
    """
    Si la función recibe una lista vacía, no puede normalizar nada.
    En ese caso debe devolver un diccionario con clave 'error'.
    """

    result = normalizar_datos_aemet([])

    assert "error" in result


# =====================================================
# TEST 4: None
# =====================================================

def test_normalizar_datos_aemet_none():
    """
    Si la función recibe None, tampoco puede procesar datos.
    Debe devolver un diccionario con clave 'error'.
    """

    result = normalizar_datos_aemet(None)

    assert "error" in result


# =====================================================
# TEST 5: valores faltantes
# =====================================================

def test_normalizar_datos_aemet_valores_faltantes(monkeypatch):
    """
    Este test comprueba qué pasa si AEMET devuelve un diccionario vacío.

    La función tiene valores por defecto:
    - estación: 'Desconocida'
    - fecha: 'N/A'
    - temperatura/humedad/viento/presión/lluvia: 0
    """

    # Simulamos una lista con un registro vacío.
    data = [{}]

    # Sustituimos alertas por lista vacía para aislar el test.
    monkeypatch.setattr(
        "services.normalizer_service.alert_service.evaluar_alertas",
        lambda x: []
    )

    # Ejecutamos la función.
    result = normalizar_datos_aemet(data)

    # Comprobamos los valores por defecto.
    assert result["estacion"] == "Ubicación Desconocida"
    assert result["fecha"] == "N/A"
    assert result["temperatura"] == 0
    assert result["humedad"] == 0
    assert result["viento"] == 0
    assert result["presion"] == 0
    assert result["lluvia"] == 0
    assert result["alertas"] == []


# =====================================================
# TEST 6: error interno controlado
# =====================================================

def test_normalizar_datos_aemet_error(monkeypatch):
    """
    Este test fuerza un error interno para comprobar que la función
    no rompe la aplicación y devuelve un diccionario con clave 'error'.

    En una app real, esto es importante porque si algo raro llega desde la API,
    queremos controlar el fallo.
    """

    # Creamos un objeto falso que parece un diccionario,
    # pero cuya función get() falla a propósito.
    class BrokenData:
        def get(self, *args, **kwargs):
            raise Exception("error forzado")

    # La función espera una lista o un diccionario.
    # Le pasamos una lista con este objeto roto para provocar el except.
    data = [BrokenData()]

    # Ejecutamos la función.
    result = normalizar_datos_aemet(data)

    # Si todo está bien controlado, no debe explotar,
    # sino devolver un diccionario con error.
    assert "error" in result