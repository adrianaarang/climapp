import json
import os

class JSONRepository:
    def __init__(self, file_path):
        self.file_path = file_path

    def guardar(self, registro_dict):
        """Método robusto para persistencia"""
        try:
            # Asegurar que el directorio existe (evita errores de ruta)
            os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
            
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
        """Busca el último registro aplicando limpieza de strings"""
        try:
            if not os.path.exists(self.file_path):
                return None
            
            # Limpieza preventiva
            municipio_buscado = municipio.strip().lower()
            
            with open(self.file_path, 'r', encoding='utf-8') as f:
                datos = json.load(f)
            
            filtrados = [
                r for r in datos 
                if r.get("municipio", "").strip().lower() == municipio_buscado 
                and r.get("fuente") == fuente
            ]
            # Devolvemos el último (más reciente)
            return filtrados[-1] if filtrados else None
        except Exception as e:
            print(f"Error al buscar último registro: {e}")
            return None

# --- CAPA DE COMPATIBILIDAD (EL PUENTE) ---
_repo = JSONRepository("data/registros_climaticos.json")

def append(registro_dict):
    return _repo.guardar(registro_dict)

def find_latest_by_municipio_and_source(municipio, fuente):
    return _repo.find_latest_by_municipio_and_source(municipio, fuente)

def filter_records(municipio=None, fecha=None):
    """Filtros inteligentes con manejo de errores"""
    if not os.path.exists(_repo.file_path):
        return []
    
    try:
        with open(_repo.file_path, 'r', encoding='utf-8') as f:
            datos = json.load(f)
    except (json.JSONDecodeError, ValueError):
        return []
    
    if municipio:
        m_clean = municipio.strip().lower()
        datos = [r for r in datos if m_clean in r.get("municipio", "").lower()]
    
    if fecha:
        # Adriana usa DD/MM/AAAA, nos aseguramos de que el startswith coincida
        datos = [r for r in datos if r.get("fecha", "").startswith(fecha)]
        
    return datos