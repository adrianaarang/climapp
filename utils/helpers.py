import math


def calcular_distancia(lat1, lon1, lat2, lon2):
    """
    Calcula la distancia en kilómetros entre dos puntos geográficos
    usando la fórmula de Haversine (teniendo en cuenta la curvatura de la Tierra)
    """

    # Paso de grados a radianes (necesario para funciones trigonométricas)
    rad = math.pi / 180

    # Diferencia de latitud y longitud en radianes
    dlat = (lat2 - lat1) * rad
    dlon = (lon2 - lon1) * rad

    # Calculo la distancia entre dos coordenadas usando Haversine, que tiene en cuenta la curvatura de la Tierra
    a = (
        math.sin(dlat / 2) ** 2 +
        math.cos(lat1 * rad) *
        math.cos(lat2 * rad) *
        math.sin(dlon / 2) ** 2
    )

    # Fórmula de Haversine (parte 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Radio de la Tierra ≈ 6371 km
    distancia = 6371 * c

    return distancia