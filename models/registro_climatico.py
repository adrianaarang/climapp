class RegistroClimatico:
    def __init__(self, estacion_id, fecha, temperatura, humedad, viento, lluvia):
        """
        Inicializa una instancia con datos climáticos previamente validados.
        Se asume que los valores númericos llegan como tipos float/int.
        """
        self.estacion_id = estacion_id
        self.fecha = fecha
        self.temperatura = temperatura
        self.humedad = humedad
        self.viento = viento
        self.lluvia = lluvia

    def to_dict(self):
        """
        Serializa el objeto a un diccionarioo.
        Facilita el almacenamiento al formato JSON y el envío de dayos a la UI
        """
        return{
            "estacion_id": self.estacion_id,
            "fecha": self.fecha,
            "temperatura": self.temperatura,
            "humedad": self.humedad,
            "viento": self.viento,
            "lluvia": self.lluvia            
        }