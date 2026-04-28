import json
import pytest
from pathlib import Path

# Importamos las funciones a testear
import repositories.json_repository as repo


# =====================================================
# FIXTURE: archivo JSON temporal
# =====================================================
# tmp_path es una carpeta temporal que pytest crea SOLO para el test.
# Así no tocamos data/registros_climaticos.json real.

@pytest.fixture
def temp_json_file(tmp_path, monkeypatch):
    
    #Crea un archivo JSON temporal y sustituye DATA_FILE
    #para que el repository use este archivo en vez del real.
    

    # Creamos un archivo temporal
    file_path = tmp_path / "test_data.json"

    # Inicializamos el archivo con lista vacía
    file_path.write_text("[]", encoding="utf-8")

    # Monkeypatch: sustituimos la ruta real por la temporal
    monkeypatch.setattr(repo, "DATA_FILE", file_path)

    return file_path


# =====================================================
# TEST load_all()
# =====================================================

def test_load_all_empty(temp_json_file):
    """
    Si el JSON está vacío, debe devolver lista vacía.
    """
    data = repo.load_all()
    assert data == []


def test_load_all_with_data(temp_json_file):
    """
    Comprueba que load_all devuelve correctamente los datos guardados.
    """
    sample_data = [{"id": "1", "municipio": "Madrid"}]

    # Escribimos datos en el JSON temporal
    temp_json_file.write_text(json.dumps(sample_data), encoding="utf-8") #json.dumps() convierte la lista de Python a formato JSON para guardarla en el archivo.

    data = repo.load_all()
    assert data == sample_data


# =====================================================
# TEST save_all()
# =====================================================

def test_save_all(temp_json_file):
    """
    Comprueba que save_all guarda correctamente los datos.
    """
    records = [{"id": "1"}]

    repo.save_all(records)

    # Leemos directamente el archivo para comprobarlo
    saved = json.loads(temp_json_file.read_text(encoding="utf-8"))

    assert saved == records


# =====================================================
# TEST append()
# =====================================================

def test_append_success(temp_json_file):
    """
    Comprueba que se añade un registro correctamente.
    """
    record = {"id": "1", "municipio": "Madrid"}

    result = repo.append(record)

    assert result["success"] is True

    data = repo.load_all()
    assert len(data) == 1


def test_append_duplicate(temp_json_file):
    """
    Comprueba que no permite duplicados.
    """
    record = {"id": "1", "municipio": "Madrid"}

    repo.append(record)
    result = repo.append(record)

    assert result["success"] is False


# =====================================================
# TEST filter_records()
# =====================================================

def test_filter_by_municipio(temp_json_file):
    """
    Comprueba que filtra correctamente por municipio.
    """
    records = [
        {"id": "1", "municipio": "Madrid", "fecha": "2026-04-22 12:00:00"},
        {"id": "2", "municipio": "Sevilla", "fecha": "2026-04-22 12:00:00"}
    ]

    repo.save_all(records)

    result = repo.filter_records(municipio="Madrid")

    assert len(result) == 1
    assert result[0]["municipio"] == "Madrid"


def test_filter_by_fecha(temp_json_file):
    """
    Comprueba que filtra correctamente por fecha.
    """
    records = [
        {"id": "1", "municipio": "Madrid", "fecha": "2026-04-22 12:00:00"},
        {"id": "2", "municipio": "Madrid", "fecha": "2026-04-23 12:00:00"}
    ]

    repo.save_all(records)

    result = repo.filter_records(fecha="2026-04-22")

    assert len(result) == 1
    assert result[0]["fecha"].startswith("2026-04-22")