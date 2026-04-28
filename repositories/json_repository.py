import json
import os
from services.logging_service import log_info, log_error

DATA_FILE = "data/registros.json"

def append(registro_dict):
    """Añade un registro y devuelve un diccionario para los tests."""
    try:
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
        datos = load_all().get("data", []) if isinstance(load_all(), dict) else load_all()

        # Evitar duplicados por ID (test_append_duplicate)
        if any(r.get('id') == registro_dict.get('id') for r in datos if 'id' in registro_dict):
            return {"success": False, "error": "ID duplicado"}

        datos.append(registro_dict)

        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump({"success": True, "data": datos}, f, indent=4, ensure_ascii=False)
        
        log_info(f"Registro guardado correctamente en {DATA_FILE}")
        return {"success": True}

    except Exception as e:
        log_error(f"Error al guardar: {e}")
        return {"success": False, "error": str(e)}

def load_all():
    """Carga todos los registros del JSON."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []

def save_all(records):
    """Guarda una lista completa de registros."""
    try:
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(records, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        log_error(f"Error en save_all: {e}")
        return False

def filter_records(municipio=None, fecha=None):
    """
    Función unificada de filtrado que espera el test de Elena.
    Permite filtrar por municipio, por fecha o ambos.
    """
    datos = load_all()
    resultado = datos

    if municipio:
        resultado = [r for r in resultado if r.get('municipio') == municipio]
    
    if fecha:
        # El test busca que la cadena de fecha esté contenida (ej: '2026-04-22')
        resultado = [r for r in resultado if fecha in r.get('fecha', '')]
    
    return {"success": True, "data": resultado}