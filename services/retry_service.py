import logging
from requests import Session
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

def get_retry_session(retries: int = 3, backoff_factor: float = 1.5) -> Session:
    """
    Configura una sesión de requests con reintentos automáticos para errores transitorios.
    
    Args:
        retries (int): Número total de reintentos permitidos.
        backoff_factor (float): Factor de espera exponencial (ej. 1.5s, 3s, 4.5s...).
        
    Returns:
        Session: Objeto sesión de requests configurado con la estrategia de Retry.
    """
    session = Session()
    retry_strategy = Retry(
        total=retries,
        backoff_factor=backoff_factor,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session