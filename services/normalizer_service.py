import json
import os
from typing import Dict, Any

class NormalizerService:
    """
    Servicio para la normalización de datos al Contrato de Adriana.
    
    Campos: fecha, municipio, codigo_municipio, temperatura, humedad, viento, lluvia, fuente, alertas.
    """

    def __init__(self, municipios_path: str = "config/municipios.json"):
        self.municipios_map = self._load_municipios(municipios_path)

    def _load_municipios(self, path: str) -> Dict[str, str]:
        """Carga el mapeo oficial de IDs y nombres de municipios."""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # Logica de fallback mínima por seguridad si el archivo falta
            return {}

    def _parse_float(self, value: Any) -> float:
        """
        Convierte valores a float manejando casos nulos e 'Ip' (Inapreciable).
        """
        if value is None:
            return 0.0
        
        if isinstance(value, str):
            if value.strip().lower() == "ip":
                return 0.0
            try:
                return float(value.replace(',', '.'))
            except ValueError:
                return 0.0
                
        return float(value)

    def normalizar_respuesta_aemet(self, datos_crudos: Dict[str, Any], station_id: str) -> Dict[str, Any]:
        """
        Transforma el JSON de AEMET al formato estándar de Climapp.
        
        Args:
            datos_crudos (Dict[str, Any]): Datos directos de la API.
            station_id (str): Identificador de la estación.
            
        Returns:
            Dict[str, Any]: Diccionario bajo el contrato de datos oficial.
        """
        # Formateo de fecha: AEMET (fint) '2023-10-27T10:00:00' -> 'YYYY-MM-DD HH:mm:ss'
        fecha_iso = datos_crudos.get("fint", "")
        # Limpiamos la T y los posibles desfases de zona horaria para cumplir el contrato
        fecha_formateada = fecha_iso.replace('T', ' ').split('+')[0] if fecha_iso else "N/A"

        # Mapeo de campos según contrato Adriana
        return {
            "fecha": fecha_formateada,
            "municipio": self.municipios_map.get(station_id, "Municipio Desconocido"),
            "codigo_municipio": station_id,
            "temperatura": self._parse_float(datos_crudos.get("ta")),
            "humedad": int(self._parse_float(datos_crudos.get("hr"))),
            "viento": self._parse_float(datos_crudos.get("vv")),
            "lluvia": self._parse_float(datos_crudos.get("prec")),
            "fuente": "api_aemet",
            "alertas": []
        }