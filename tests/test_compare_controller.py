import pytest

# Importamos las funciones que queremos probar desde compare_controller.py
from controllers.compare_controller import (
    calculate_difference,
    has_discrepancy,
    compare_latest_records
)


# =====================================================
# FIXTURES
# =====================================================
# Una fixture es una función que prepara datos de prueba
# para reutilizarlos en varios tests.
# Así no tenemos que copiar el mismo diccionario muchas veces.


@pytest.fixture
def manual_record():
    
    #Registro manual ficticio para usar en los tests.
    #Simula un dato introducido por una persona.
    
    return {
        "id": "manual_1",
        "fecha": "2026-04-22 12:00:00",
        "municipio": "Madrid",
        "temperatura": 23.5,
        "humedad": 60,
        "viento": 10.0,
        "lluvia": 0,
        "fuente": "manual"
    }


@pytest.fixture
def api_record():
    #Registro API ficticio para usar en los tests.
    #Simula un dato recibido automáticamente desde AEMET.
    
    return {
        "id": "api_1",
        "fecha": "2026-04-22 12:30:00",
        "municipio": "Madrid",
        "temperatura": 22.4,
        "humedad": 58,
        "viento": 12.1,
        "lluvia": 0,
        "fuente": "api_aemet"
    }


# =====================================================
# TESTS DE FUNCIONES PEQUEÑAS
# =====================================================


def test_calculate_difference():
    
    #Comprueba que calculate_difference calcula bien
    #la diferencia absoluta entre dos números.
    
    result = calculate_difference(10, 8)

    # Esperamos que la diferencia entre 10 y 8 sea 2
    assert result == 2


def test_calculate_difference_rounding():
   
    #Comprueba que calculate_difference redondea correctamente
    #la diferencia a 2 decimales.
    
    result = calculate_difference(22.4, 23.5)

    # Sin redondeo, Python podría devolver 1.1000000000000014.
    # Con nuestro código esperamos 1.1.
    assert result == 1.1


def test_has_discrepancy_true():
   
    #Comprueba que has_discrepancy devuelve True
    #cuando alguna diferencia supera los umbrales definidos.
    
    differences = {
        "temperatura": 4,
        "humedad": 1,
        "viento": 0,
        "lluvia": 0
    }

    # Como temperatura es mayor que 3, debe haber discrepancia.
    assert has_discrepancy(differences) is True


def test_has_discrepancy_false():
   
    #Comprueba que has_discrepancy devuelve False
    #cuando ninguna diferencia supera los umbrales.
   
    differences = {
        "temperatura": 1,
        "humedad": 1,
        "viento": 0,
        "lluvia": 0
    }

    # Ninguna diferencia supera el umbral, así que no hay discrepancia.
    assert has_discrepancy(differences) is False


# =====================================================
# TESTS DE compare_latest_records CON MONKEYPATCH
# =====================================================
# compare_latest_records necesita consultar datos en el repository.
# Para no depender del archivo JSON real, usamos monkeypatch.Se usa para evitar dependencias externas(json, apis)
# Controlamos el flujo de datos en los tests,sustituyendo funciones reales por otras simuladas, 
# para no depender de APIs, archivos json, bases de datos, etc. Esto hace que los tests sean más rápidos y fiables.
# monkeypatch sustituye temporalmente solo para los test,una función real por una falsa.
# En este caso sustituimos find_latest_by_municipio_and_source()
# por una función fake que devuelve datos preparados por nosotras.



def test_compare_latest_records_success(monkeypatch, manual_record, api_record):
    """
    Comprueba que compare_latest_records funciona correctamente
    cuando existen tanto el registro manual como el registro API.
    """

    # Creamos una función falsa que simula el comportamiento del repository.
    # Si se pide fuente manual, devuelve manual_record.
    # Si se pide fuente api_aemet, devuelve api_record.
    def fake_find_latest(municipio, fuente):
        if fuente == "manual":
            return manual_record

        if fuente == "api_aemet":
            return api_record

        return None

    # Sustituimos la función real del compare_controller
    # por nuestra función falsa.
    monkeypatch.setattr(
        "controllers.compare_controller.find_latest_by_municipio_and_source",
        fake_find_latest
    )

    # Ejecutamos la función principal de comparativa.
    result = compare_latest_records("Madrid")

    # Comprobamos que la comparación fue exitosa.
    assert result["success"] is True

    # Comprobamos que el municipio devuelto es correcto.
    assert result["municipio"] == "Madrid"

    # Comprobamos que devuelve el bloque de diferencias.
    assert "diferencias" in result

    # Comprobamos que indica si hay o no discrepancia.
    assert "hay_discrepancia" in result

    # Comprobamos una diferencia concreta.
    assert result["diferencias"]["temperatura"] == 1.1


def test_compare_latest_records_no_manual(monkeypatch, api_record):
    """
    Comprueba que compare_latest_records devuelve error
    si no existe registro manual.
    """

    # Función falsa:
    # - para manual devuelve None
    # - para api_aemet devuelve api_record
    def fake_find_latest(municipio, fuente):
        if fuente == "manual":
            return None

        if fuente == "api_aemet":
            return api_record

        return None

    # Sustituimos la función real por la falsa.
    monkeypatch.setattr(
        "controllers.compare_controller.find_latest_by_municipio_and_source",
        fake_find_latest
    )

    # Ejecutamos la comparación.
    result = compare_latest_records("Madrid")

    # Debe fallar porque falta el dato manual.
    assert result["success"] is False

    # El mensaje debe mencionar el registro manual.
    assert "manual" in result["message"].lower()


def test_compare_latest_records_no_api(monkeypatch, manual_record):
    """
    Comprueba que compare_latest_records devuelve error
    si no existe registro API AEMET.
    """

    # Función falsa:
    # - para manual devuelve manual_record
    # - para api_aemet devuelve None
    def fake_find_latest(municipio, fuente):
        if fuente == "manual":
            return manual_record

        if fuente == "api_aemet":
            return None

        return None

    # Sustituimos la función real por la falsa.
    monkeypatch.setattr(
        "controllers.compare_controller.find_latest_by_municipio_and_source",
        fake_find_latest
    )

    # Ejecutamos la comparación.
    result = compare_latest_records("Madrid")

    # Debe fallar porque falta el dato API.
    assert result["success"] is False

    # El mensaje debe mencionar API.
    assert "api" in result["message"].lower()


    #para probar py -m pytest tests/test_compare_controller.py tests/test_json_repository.py -v