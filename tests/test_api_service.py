import pytest

# Importamos la clase que queremos probar.
# Esta clase está en services/weather_api_service.py
from services.weather_api_service import WeatherAPIService


# =====================================================
# CLASE FAKE: respuesta HTTP simulada
# =====================================================

class FakeResponse:
    """
    Esta clase simula una respuesta HTTP como las que devuelve requests.

    La usamos para no llamar realmente a AEMET durante los tests.
    """

    def __init__(self, json_data):
        """
        Guardamos el JSON falso que queremos que devuelva esta respuesta.
        """
        self.json_data = json_data

    def raise_for_status(self):
        """
        En requests, raise_for_status() lanza error si la respuesta HTTP falla.

        Aquí no queremos que falle, así que simplemente no hace nada.
        """
        return None

    def json(self):
        """
        Simula el método .json() de requests.

        Devuelve los datos falsos que hemos preparado.
        """
        return self.json_data


# =====================================================
# CLASE FAKE: sesión HTTP simulada
# =====================================================

class FakeSession:
    """
    Esta clase simula la sesión HTTP que usa WeatherAPIService.

    En el código real, el servicio hace dos peticiones:
    1. A la URL base de AEMET.
    2. A la URL de datos que devuelve AEMET.

    Aquí simulamos esas dos llamadas.
    """

    def __init__(self):
        """
        Contador para saber si estamos en la primera o segunda llamada.
        """
        self.calls = 0

    def get(self, url, headers=None, timeout=20):
        """
        Simula el método get() de una sesión HTTP.

        Dependiendo de cuántas veces se haya llamado, devuelve una cosa u otra.
        """

        self.calls += 1

        # Primera llamada:
        # AEMET no devuelve directamente los datos.
        # Primero devuelve un JSON con una URL dentro de la clave "datos".
        if self.calls == 1:
            return FakeResponse({
                "datos": "https://fake-url-aemet/datos"
            })

        # Segunda llamada:
        # Simulamos la respuesta real con observaciones meteorológicas.
        return FakeResponse([
            {
                "ubi": "Madrid-Retiro",
                "lat": "40.4168",
                "lon": "-3.7038",
                "ta": "22.5"
            },
            {
                "ubi": "Barcelona",
                "lat": "41.3874",
                "lon": "2.1686",
                "ta": "20.1"
            }
        ])


# =====================================================
# FIXTURE: servicio API preparado para tests
# =====================================================

@pytest.fixture
def api_service(monkeypatch):
    """
    Esta fixture prepara una instancia de WeatherAPIService
    sin usar datos reales.

    Hace dos cosas importantes:

    1. Crea una API key falsa.
       Así evitamos depender de un archivo .env real.

    2. Sustituye get_retry_session() por una sesión falsa.
       Así evitamos hacer llamadas reales a internet.
    """

    # Simulamos que existe la variable de entorno AEMET_API_KEY.
    # El servicio real la necesita para inicializarse.
    monkeypatch.setenv("AEMET_API_KEY", "fake_api_key")

    # Sustituimos get_retry_session por una función falsa
    # que devuelve FakeSession.
    monkeypatch.setattr(
        "services.weather_api_service.get_retry_session",
        lambda: FakeSession()
    )

    # Devolvemos el servicio ya preparado para los tests.
    return WeatherAPIService()


# =====================================================
# TEST 1: inicialización correcta
# =====================================================

def test_weather_api_service_init(api_service):
    """
    Comprueba que WeatherAPIService se inicializa correctamente
    cuando existe la variable AEMET_API_KEY.
    """

    assert api_service.api_key == "fake_api_key"

    assert api_service.base_url == (
        "https://opendata.aemet.es/opendata/api/observacion/convencional/todas"
    )


# =====================================================
# TEST 2: error si no hay API KEY
# =====================================================

def test_weather_api_service_no_api_key(monkeypatch):
    """
    Comprueba que el servicio lanza ValueError
    si no existe AEMET_API_KEY.

    Esto es importante porque sin API key no se puede consultar AEMET.
    """

    # Eliminamos la variable de entorno si existe.
    monkeypatch.delenv("AEMET_API_KEY", raising=False)

    # Esperamos que al crear el servicio se lance ValueError.
    with pytest.raises(ValueError):
        WeatherAPIService()


# =====================================================
# TEST 3: obtener datos crudos correctamente
# =====================================================

def test_obtener_datos_crudos_success(api_service):
    """
    Comprueba que _obtener_datos_crudos() devuelve una lista
    de observaciones cuando las respuestas simuladas son correctas.
    """

    result = api_service._obtener_datos_crudos()

    # Debe devolver una lista.
    assert isinstance(result, list)

    # En FakeSession hemos preparado 2 observaciones.
    assert len(result) == 2

    # Comprobamos que la primera observación es Madrid-Retiro.
    assert result[0]["ubi"] == "Madrid-Retiro"


# =====================================================
# TEST 4: primera respuesta sin clave "datos"
# =====================================================

def test_obtener_datos_crudos_sin_url_datos(monkeypatch):
    """
    Comprueba que si la primera respuesta de AEMET no trae
    la clave 'datos', la función devuelve lista vacía.

    Esto simula una respuesta incompleta o inesperada de la API.
    """

    class FakeSessionNoDatos:
        """
        Sesión falsa que devuelve un JSON sin la clave 'datos'.
        """

        def get(self, url, headers=None, timeout=20):
            return FakeResponse({})

    # Simulamos API key.
    monkeypatch.setenv("AEMET_API_KEY", "fake_api_key")

    # Sustituimos la sesión real por la falsa.
    monkeypatch.setattr(
        "services.weather_api_service.get_retry_session",
        lambda: FakeSessionNoDatos()
    )

    service = WeatherAPIService()

    result = service._obtener_datos_crudos()

    assert result == []


# =====================================================
# TEST 5: error en la petición
# =====================================================

def test_obtener_datos_crudos_error(monkeypatch):
    """
    Comprueba que si ocurre un error durante la petición,
    la función no rompe la aplicación.

    En vez de lanzar error, debe devolver lista vacía.
    """

    class FakeSessionError:
        """
        Sesión falsa que lanza una excepción al hacer get().
        """

        def get(self, *args, **kwargs):
            raise Exception("Error simulado")

    # Simulamos API key.
    monkeypatch.setenv("AEMET_API_KEY", "fake_api_key")

    # Sustituimos la sesión real por una que falla.
    monkeypatch.setattr(
        "services.weather_api_service.get_retry_session",
        lambda: FakeSessionError()
    )

    service = WeatherAPIService()

    result = service._obtener_datos_crudos()

    assert result == []


# =====================================================
# TEST 6: estación más cercana por coordenadas
# =====================================================

def test_obtener_clima_por_coordenadas_devuelve_estacion_cercana(api_service):
    """
    Comprueba que obtener_clima_por_coordenadas()
    devuelve la estación más cercana a las coordenadas dadas.

    Usamos las coordenadas de Madrid, por lo que esperamos Madrid-Retiro.
    """

    result = api_service.obtener_clima_por_coordenadas(40.4168, -3.7038)

    assert result is not None
    assert result["ubi"] == "Madrid-Retiro"


# =====================================================
# TEST 7: sin observaciones
# =====================================================

def test_obtener_clima_por_coordenadas_sin_observaciones(monkeypatch, api_service):
    """
    Comprueba que si no hay observaciones de AEMET,
    la función devuelve None.
    """

    # Sustituimos _obtener_datos_crudos para que devuelva lista vacía.
    monkeypatch.setattr(
        api_service,
        "_obtener_datos_crudos",
        lambda: []
    )

    result = api_service.obtener_clima_por_coordenadas(40.4168, -3.7038)

    assert result is None


# =====================================================
# TEST 8: ignorar datos corruptos
# =====================================================

def test_obtener_clima_por_coordenadas_ignora_datos_corruptos(monkeypatch, api_service):
    """
    Comprueba que el servicio ignora observaciones con coordenadas corruptas.

    Si una estación trae latitud o longitud inválida, se salta.
    """

    observaciones = [
        {
            "ubi": "Estación corrupta",
            "lat": "no_valido",
            "lon": "-3.7"
        },
        {
            "ubi": "Madrid-Retiro",
            "lat": "40.4168",
            "lon": "-3.7038"
        }
    ]

    # Forzamos que _obtener_datos_crudos devuelva nuestras observaciones falsas.
    monkeypatch.setattr(
        api_service,
        "_obtener_datos_crudos",
        lambda: observaciones
    )

    result = api_service.obtener_clima_por_coordenadas(40.4168, -3.7038)

    assert result is not None
    assert result["ubi"] == "Madrid-Retiro"


# =====================================================
# TEST 9: método obtener_clima_por_id
# =====================================================

def test_obtener_clima_por_id_devuelve_none(api_service):
    """
    Actualmente obtener_clima_por_id() está vacío con pass.

    En Python, una función con pass devuelve None.
    """

    assert api_service.obtener_clima_por_id("1234") is None