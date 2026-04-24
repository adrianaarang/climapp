from repositories.json_repository import find_latest_by_municipio_and_source
from services.logging_service import log_info, log_error


def calculate_difference(value_1: float, value_2: float) -> float:
    """
    Devuelve la diferencia absoluta entre dos valores,
    redondeada a 2 decimales.
    """
    return round(abs(value_1 - value_2), 2)


def has_discrepancy(differences: dict) -> bool:
    """
    Comprueba si las diferencias son lo bastante grandes
    como para considerarlas una discrepancia importante.
    """

    if differences["temperatura"] > 3:
        return True

    if differences["humedad"] > 10:
        return True

    if differences["viento"] > 10:
        return True

    if differences["lluvia"] > 5:
        return True

    return False

def compare_latest_records(municipio: str) -> dict:
    """
    Compara el último registro manual con el último registro API AEMET
    de un municipio concreto.
    """

    manual_record = find_latest_by_municipio_and_source(municipio, "manual")
    api_record = find_latest_by_municipio_and_source(municipio, "api_aemet")

    if manual_record is None:
        log_error(f"No hay registro manual para el municipio '{municipio}'.")
        return {
            "success": False,
            "message": f"No hay registro manual para el municipio '{municipio}'."
        }

    if api_record is None:
        log_error(f"No hay registro de API para el municipio '{municipio}'.")
        return {
            "success": False,
            "message": f"No hay registro de API para el municipio '{municipio}'."
        }

    differences = {
        "temperatura": calculate_difference(
            manual_record.get("temperatura", 0),
            api_record.get("temperatura", 0)
        ),
        "humedad": calculate_difference(
            manual_record.get("humedad", 0),
            api_record.get("humedad", 0)
        ),
        "viento": calculate_difference(
            manual_record.get("viento", 0),
            api_record.get("viento", 0)
        ),
        "lluvia": calculate_difference(
            manual_record.get("lluvia", 0),
            api_record.get("lluvia", 0)
        )
    }

    discrepancy = has_discrepancy(differences)

    log_info(f"Comparativa realizada correctamente para el municipio '{municipio}'.")

    return {
        "success": True,
        "municipio": municipio,
        "manual": manual_record,
        "api": api_record,
        "diferencias": differences,
        "hay_discrepancia": discrepancy
    }