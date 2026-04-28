import json
import os
from services.logging_service import log_info, log_error

# Ruta por defecto para los datos
DATA_FILE = "data/registros.json"

def append(registro_dict):
    """Añade un registro al archivo JSON y lo guarda."""
    try:
        # Asegurar que la carpeta data existe
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)

        datos = []
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                try:
                    datos = json.load(f)
                except json.JSONDecodeError:
                    datos = []

        datos.append(registro_dict)

        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)
        
        log_info(f"Registro guardado correctamente en {DATA_FILE}")
        return True

    except Exception as e:
        log_error(f"Error al guardar en el repositorio JSON: {e}")
        return False

def load_all():
    """Carga todos los registros del JSON."""
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)