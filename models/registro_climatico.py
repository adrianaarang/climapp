class RegistroClimatico:
    def __init__(self, estacion_id, fecha, temperatura, humedad, viento, lluvia):
        """
        Aqui se inicializan los datos que ya han sido filtrados por validación
        """
        self.estacion_id = estacion_id
        self.fecha = fecha
        self.temperatura = temperatura
        self.humedad = humedad
        self.viento = viento
        self.lluvia = lluvia

    def to_dict(self):
        """Convierte el código a diccionario para guardarlo en el JSON."""
        return{
            "estacion_id": self.estacion_id,
            "fecha": self.fecha,
            "temperatura": self.temperatura,
            "humedad": self.humedad,
            "viento": self.viento,
            "lluvia": self.lluvia            
        }