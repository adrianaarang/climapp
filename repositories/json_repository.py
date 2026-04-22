import json
from pathlib import Path
from typing import Optional

from services.logging_service import log_info, log_warning, log_error


# Ruta del archivo JSON donde se guardan los registros climáticos
DATA_FILE = Path("data/registros_climaticos.json")


def load_all() -> list:
    """
    Carga todos los registros almacenados en el archivo JSON.

    Devuelve:
        list -> lista de registros
                si el archivo no existe o está mal, devuelve []
    """

    # Si el archivo todavía no existe, devolvemos lista vacía
    if not DATA_FILE.exists():
        log_warning("El archivo de registros no existe todavía. Se devuelve una lista vacía.")
        return []

    try:
        # Abrimos el archivo en modo lectura
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        # Comprobamos que el contenido sea una lista
        if isinstance(data, list):
            return data

        # Si no es una lista, devolvemos lista vacía
        log_error("El contenido del archivo JSON no es una lista válida.")
        return []

    except json.JSONDecodeError:
        # El JSON existe pero está mal escrito o corrupto
        log_error("Error al leer el archivo JSON: formato inválido o archivo corrupto.")
        return []

    except OSError as error:
        # Error general al leer el archivo
        log_error(f"Error del sistema al intentar leer el archivo JSON: {error}")
        return []


def save_all(records: list) -> None:
    """
    Guarda todos los registros en el archivo JSON.

    Parámetros:
        records (list): lista completa de registros
    """

    # Creamos la carpeta data/ si no existe
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

    try:
        # Abrimos el archivo en modo escritura
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            # Guardamos los datos en formato JSON legible
            json.dump(records, file, ensure_ascii=False, indent=4)

        log_info("Registros guardados correctamente en el archivo JSON.")

    except OSError as error:
        log_error(f"Error al guardar registros en el archivo JSON: {error}")


def record_exists(record_id: str, records: list) -> bool:
    """
    Comprueba si ya existe un registro con ese ID.

    Parámetros:
        record_id (str): identificador único del registro
        records (list): lista de registros ya guardados

    Devuelve:
        bool -> True si existe, False si no
    """

    # Recorremos todos los registros y comprobamos si alguno tiene el mismo id
    return any(record.get("id") == record_id for record in records)


def append(record: dict) -> dict:
    """
    Añade un nuevo registro al JSON si no está duplicado.

    Parámetros:
        record (dict): registro climático a guardar

    Devuelve:
        dict -> resultado de la operación
    """

    # Cargamos todos los registros existentes
    records = load_all()

    # Obtenemos el id del nuevo registro
    record_id = record.get("id")

    # Si no tiene id, no podemos controlar duplicados
    if not record_id:
        log_error("Se intentó guardar un registro sin campo 'id'.")
        return {
            "success": False,
            "message": "El registro no tiene campo 'id'."
        }

    # Si ese id ya existe, no lo guardamos
    if record_exists(record_id, records):
        log_warning(f"Registro duplicado detectado: {record_id}")
        return {
            "success": False,
            "message": f"El registro con id '{record_id}' ya existe."
        }

    # Si no existe, lo añadimos a la lista
    records.append(record)

    # Guardamos la lista actualizada
    save_all(records)

    log_info(f"Registro guardado correctamente: {record_id}")

    return {
        "success": True,
        "message": "Registro guardado correctamente.",
        "record_id": record_id
    }


def find_latest_by_municipio_and_source(municipio: str, fuente: str) -> Optional[dict]:
    """
    Busca el registro más reciente de un municipio y una fuente concretas.

    Parámetros:
        municipio (str): nombre del municipio. Ejemplo: 'Madrid'
        fuente (str): fuente del dato. Ejemplo: 'manual' o 'api_aemet'

    Devuelve:
        dict -> el registro más reciente
        None -> si no encuentra ninguno
    """

    # Cargamos todos los registros
    records = load_all()

    # Filtramos solo los registros que coincidan con municipio y fuente
    filtered = [
        record for record in records
        if record.get("municipio") == municipio and record.get("fuente") == fuente
    ]

    # Si no hay resultados, devolvemos None
    if not filtered:
        log_warning(f"No se encontraron registros para municipio='{municipio}' y fuente='{fuente}'.")
        return None

    # Ordenamos de más reciente a más antiguo usando la fecha
    filtered.sort(key=lambda record: record.get("fecha", ""), reverse=True)

    # Guardamos el más reciente
    latest_record = filtered[0]

    log_info(
        f"Último registro encontrado para municipio='{municipio}' y fuente='{fuente}': "
        f"{latest_record.get('id', 'sin_id')}"
    )

    return latest_record


def filter_records(municipio: Optional[str] = None, fecha: Optional[str] = None) -> list:
    """
    Filtra registros por municipio y/o fecha.

    Parámetros:
        municipio (str | None): nombre del municipio
        fecha (str | None): fecha o parte de la fecha. Ejemplo: '2026-04-22'

    Devuelve:
        list -> lista de registros filtrados
    """

    # Cargamos todos los registros
    records = load_all()

    # Filtramos por municipio si se ha indicado
    if municipio:
        records = [
            record for record in records
            if record.get("municipio") == municipio
        ]

    # Filtramos por fecha si se ha indicado
    if fecha:
        records = [
            record for record in records
            if record.get("fecha", "").startswith(fecha)
        ]

    log_info(
        f"Filtro aplicado sobre registros. "
        f"municipio='{municipio}', fecha='{fecha}', resultados={len(records)}"
    )

    return records