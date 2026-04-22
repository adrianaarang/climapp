from typing import Dict, Any, List

try:
    from utils.validators import validate_weather_data
except ImportError:
    # Placeholder for development if utils.validators is not yet fully implemented
    print("WARNING: Could not import 'validate_weather_data' from 'utils.validators'. Using a dummy validator.")
    def validate_weather_data(data: Dict[str, Any]) -> bool:
        # Dummy implementation: always return True for now, assuming valid data for alert processing
        return True

class AlertService:
    """Motor de análisis de riesgos climáticos y generación de alertas."""

    def evaluar_alertas(self, registro_normalizado: Dict[str, Any]) -> List[str]:
        """
        Analiza un registro y genera alertas basadas en umbrales técnicos.
        
        Args:
            registro_normalizado (Dict[str, Any]): Registro tras el proceso de normalización.
            
        Returns:
            List[str]: Lista de etiquetas de alerta activas.
        """
        # 1. Validación previa obligatoria
        if not validate_weather_data(registro_normalizado):
            return []

        alertas = []
        temp = registro_normalizado.get("temperatura", 0.0)
        viento = registro_normalizado.get("viento", 0.0)
        lluvia = registro_normalizado.get("lluvia", 0.0)
        humedad = registro_normalizado.get("humedad", 0)

        # 2. Lógica de Temperatura (Jerarquía Excluyente)
        if temp >= 40.0:  # Umbral Crítico Calor
            alertas.append("ROJA")
        elif temp >= 35.0:  # Umbral Advertencia Calor
            alertas.append("NARANJA")
        elif temp <= 0.0:  # Umbral Helada
            alertas.append("HELADA")

        # 3. Lógica Independiente (Acumulativa)
        if viento > 70.0:
            alertas.append("VIENTO_FUERTE")
        if lluvia > 30.0:
            alertas.append("LLUVIA_INTENSA")
        if humedad >= 90:
            alertas.append("HUMEDAD_ALTA")

        return alertas
