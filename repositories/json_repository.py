import json
import os

class JSONRepository:
    def __init__(self, file_path):
        self.file_path = file_path

    def guardar(self, registro_dict):
        """Método original de Elena"""
        try:
            if os.path.exists(self.file_path):
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    try:
                        datos = json.load(f)
                    except json.JSONDecodeError:
                        datos = []
            else:
                datos = []

            datos.append(registro_dict)

            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(datos, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error crítico en el repositorio: {e}")
            return False

    def find_latest_by_municipio_and_source(self, municipio, fuente):
        """Busca el último registro para la comparación"""
        try:
            if not os.path.exists(self.file_path):
                return None
            with open(self.file_path, 'r', encoding='utf-8') as f:
                datos = json.load(f)
            
            filtrados = [
                r for r in datos 
                if r.get("municipio", "").lower() == municipio.lower() 
                and r.get("fuente") == fuente
            ]
            return filtrados[-1] if filtrados else None
        except Exception as e:
            print(f"Error al buscar último registro: {e}")
            return None

# --- CAPA DE COMPATIBILIDAD (EL PUENTE) ---
# Creamos la instancia que usará toda la app
_repo = JSONRepository("data/registros_climaticos.json")

# 1. Para manual_controller.py (que busca 'append')
def append(registro_dict):
    return _repo.guardar(registro_dict)

# 2. Para compare_controller.py (que busca 'find_latest_by_municipio_and_source')
def find_latest_by_municipio_and_source(municipio, fuente):
    return _repo.find_latest_by_municipio_and_source(municipio, fuente)

# 3. Para view_controller.py (que busca 'filter_records')
def filter_records(municipio=None, fecha=None):
    if not os.path.exists(_repo.file_path):
        return []
    with open(_repo.file_path, 'r', encoding='utf-8') as f:
        datos = json.load(f)
    
    if municipio:
        datos = [r for r in datos if municipio.lower() in r.get("municipio", "").lower()]
    if fecha:
        datos = [r for r in datos if r.get("fecha", "").startswith(fecha)]
    return datos