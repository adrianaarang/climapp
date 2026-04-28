import os
import logging
from typing import Dict, Any, Optional
from services.retry_service import get_retry_session
from utils.helpers import calcular_distancia

class WeatherAPIService:
    def __init__(self):
        # 1. MANTENEMOS: La configuración de Adriana e Isabela
        self.api_key = os.getenv("AEMET_API_KEY")
        if not self.api_key:
            raise ValueError("AEMET_API_KEY no encontrada en .env")
        
        self.session = get_retry_session()
        self.logger = logging.getLogger(__name__)
        self.base_url = "https://opendata.aemet.es/opendata/api/observacion/convencional/todas"

    def _obtener_datos_crudos(self) -> list:
        """Método interno para bajar todas las observaciones de AEMET."""
        headers = {"api_key": self.api_key, "cache-control": "no-cache"}
        try:
            # Usamos la sesión con reintentos de la arquitectura original
            res_meta = self.session.get(self.base_url, headers=headers, timeout=20)
            res_meta.raise_for_status()
            
            datos_url = res_meta.json().get("datos")
            if not datos_url:
                return []

            res_datos = self.session.get(datos_url, timeout=20)
            res_datos.raise_for_status()
            return res_datos.json()
        except Exception as e:
            self.logger.error(f"Error al conectar con AEMET: {e}")
            return []

    # 2. TU MEJORA: Búsqueda por coordenadas integrada
    def obtener_clima_por_coordenadas(self, user_lat: float, user_lon: float) -> Optional[Dict[str, Any]]:
        """
        Lógica de Juan: Localiza la estación más cercana y devuelve sus datos RAW.
        """
        observaciones = self._obtener_datos_crudos()
        
        if not observaciones:
            self.logger.warning("No se recibieron observaciones de AEMET.")
            return None

        estacion_cercana = None
        distancia_minima = float('inf')

        for obs in observaciones:
            try:
                # Extraemos y validamos coordenadas de la estación
                obs_lat = float(obs['lat'])
                obs_lon = float(obs['lon'])

                dist = calcular_distancia(
                    float(user_lat), 
                    float(user_lon), 
                    obs_lat, 
                    obs_lon
                )

                if dist < distancia_minima:
                    distancia_minima = dist
                    estacion_cercana = obs

            except (KeyError, ValueError, TypeError):
                continue # Saltamos estaciones con datos corruptos

        if estacion_cercana:
            self.logger.info(f"Estación más cercana hallada: {estacion_cercana.get('ubi')} a {distancia_minima:.2f}km")
        
        return estacion_cercana

    # 3. MANTENEMOS: Los métodos originales que ellas ya tuvieran (ej: por ID)
    def obtener_clima_por_id(self, station_id: str):
        # Aquí iría el código que ellas ya escribieron (puedes completarlo si es necesario)
        pass

# --- FUNCIÓN PUENTE PARA COMPATIBILIDAD CON APP.PY ---
def obtener_clima_por_coordenadas(lat, lon):
    """
    Permite que app.py siga llamando a esta función directamente 
    mientras nosotros usamos la lógica de la clase por debajo.
    """
    service = WeatherAPIService()
    return service.obtener_clima_por_coordenadas(lat, lon)