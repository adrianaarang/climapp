import os
import requests
import logging
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from services.retry_service import get_retry_session

load_dotenv()

class WeatherAPIService:
    """Servicio para la integración con AEMET OpenData siguiendo el flujo de dos pasos."""

    def __init__(self):
        self.api_key = os.getenv("AEMET_API_KEY")
        self.base_url = "https://opendata.aemet.es/opendata/api/observacion/convencional/datos/estacion/"
        self.logger = logging.getLogger(__name__)
        self.session = get_retry_session()
        
        # IDs de Estación validados según directiva de Madrid
        self.estaciones_validas = ["3195", "3100B", "2462", "3100", "3200"]

    def fetch_station_data(self, station_id: str) -> Optional[Dict[str, Any]]:
        """
        Ejecuta el flujo de dos pasos para obtener datos de una estación.
        
        Args:
            station_id (str): ID de la estación meteorológica.
            
        Returns:
            Optional[Dict[str, Any]]: El registro más reciente o None en caso de error.
        """
        if not self.api_key:
            self.logger.error("AEMET_API_KEY no configurada.")
            return None

        url_paso_1 = f"{self.base_url}{station_id}"
        headers = {
            'cache-control': "no-cache",
            'api_key': self.api_key
        }

        try:
            # Paso 1: Petición de URL de descarga
            response_1 = self.session.get(url_paso_1, headers=headers, timeout=15)
            response_1.raise_for_status()
            
            meta_res = response_1.json()
            if meta_res.get("estado") != 200:
                self.logger.warning(f"AEMET respondió con error: {meta_res.get('descripcion')}")
                return None

            url_datos = meta_res.get("datos")
            
            # Paso 2: Descarga de datos reales
            response_2 = self.session.get(url_datos, timeout=15)
            response_2.raise_for_status()
            
            datos = response_2.json()
            
            # Retornamos la observación más reciente (última en la lista de AEMET)
            if isinstance(datos, list) and len(datos) > 0:
                return datos[-1]
            
            return None

        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error de conexión con AEMET (Estación {station_id}): {e}")
            return None
        except (ValueError, KeyError) as e:
            self.logger.error(f"Error procesando formato de respuesta AEMET: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Error inesperado en WeatherAPIService: {e}")
            return None