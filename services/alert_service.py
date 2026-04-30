import logging
from typing import Dict, Any, List

try:
    from utils.validators import validate_weather_data
except ImportError:
    logger = logging.getLogger(__name__)
    logger.warning("No se pudo importar 'validate_weather_data'. Usando validador temporal.")

    def validate_weather_data(data: Dict[str, Any]) -> bool:
        return True


class AlertService:
    """Motor de análisis de riesgos climáticos y generación de alertas."""

    def evaluar_alertas(self, registro_normalizado: Dict[str, Any]) -> List[str]:

        if not validate_weather_data(registro_normalizado):
            return []

        alertas = []

        try:
            temp = float(registro_normalizado.get("temperatura", 0.0))
            viento = float(registro_normalizado.get("viento", 0.0))
            lluvia = float(registro_normalizado.get("lluvia", 0.0))
            humedad = float(registro_normalizado.get("humedad", 0.0))

        except (TypeError, ValueError):
            return []

        # TEMPERATURA
        if temp >= 40.0:
            alertas.append("ROJA_CALOR")
        elif temp >= 35.0:
            alertas.append("NARANJA_CALOR")
        elif temp <= -5.0:
            alertas.append("ROJA_FRIO")
        elif temp <= 0.0:
            alertas.append("NARANJA_FRIO")

        # VIENTO
        if viento > 70.0:
            alertas.append("ROJA_VIENTO")
        elif viento > 40.0:
            alertas.append("NARANJA_VIENTO")

        # LLUVIA
        if lluvia > 30.0:
            alertas.append("ROJA_LLUVIA")
        elif lluvia > 10.0:
            alertas.append("NARANJA_LLUVIA")

        # HUMEDAD
        if humedad >= 90:
            alertas.append("NARANJA_HUMEDAD")

        # Si no hay ninguna alerta, devolvemos verde general
        if not alertas:
            alertas.append("VERDE")

        return alertas