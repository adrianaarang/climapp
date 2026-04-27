import json
import os

class JSONRepository:
    def __init__(self, file_path):
        self.file_path = file_path

    def guardar(self, registro_dict):
        try:
            # 1. Leer datos previos
            if os.path.exists(self.file_path):
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    try:
                        datos = json.load(f)
                    except json.JSONDecodeError:
                        datos = []
            else:
                datos = []

            # 2. Añadir nuevo
            datos.append(registro_dict)

            # 3. Escribir en el archivo
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(datos, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error crítico en el repositorio: {e}")
            return False