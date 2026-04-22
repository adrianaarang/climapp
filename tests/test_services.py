import pytest
from services.normalizer_service import NormalizerService
from services.alert_service import AlertService

def test_normalizer_handles_ip_rain():
    """Verifica que la lluvia inapreciable 'Ip' se convierta en 0.0."""
    service = NormalizerService()
    raw_data = {"fint": "2023-10-27T10:00:00", "prec": "Ip", "ta": "20", "hr": "50", "vv": "10"}
    normalized = service.normalizar_respuesta_aemet(raw_data, "3195")
    assert normalized["lluvia"] == 0.0
    assert isinstance(normalized["lluvia"], float)

def test_alert_service_red_alert():
    """Verifica que se dispare la alerta ROJA a partir de 40 grados."""
    service = AlertService()
    data = {
        "temperatura": 42.0,
        "viento": 10.0,
        "lluvia": 0.0,
        "humedad": 40
    }
    alertas = service.evaluar_alertas(data)
    assert "ROJA" in alertas

def test_alert_service_multiple_alerts():
    """Verifica que las alertas sean acumulativas (viento y lluvia)."""
    service = AlertService()
    data = {
        "temperatura": 20.0,
        "viento": 80.0,
        "lluvia": 45.0,
        "humedad": 50
    }
    alertas = service.evaluar_alertas(data)
    assert "VIENTO_FUERTE" in alertas
    assert "LLUVIA_INTENSA" in alertas
    assert len(alertas) == 2