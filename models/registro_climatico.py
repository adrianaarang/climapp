class RegistroClimatico:
    def __init__(self, estacion_id, fecha, temperatura, humedad, viento, lluvia):
        """
        Isabella, mantengo tu estructura original. He añadido pequeñas 
        conversiones de tipo (float) aquí por seguridad, para asegurarnos 
        de que si el controlador olvida convertir algo, el modelo lo arregle.
        """
        self.estacion_id = estacion_id
        self.fecha = fecha
        # Aseguramos que las métricas sean numéricas para evitar errores en cálculos futuros
        self.temperatura = float(temperatura)
        self.humedad = float(humedad)
        self.viento = float(viento)
        self.lluvia = float(lluvia)

    def to_dict(self):
        """
        Mantenemos este método tal cual lo hiciste. 
        Es perfecto para que el JSONRepository pueda guardar los datos 
        y para que el frontend reciba la respuesta correctamente.
        """
        return {
            "estacion_id": self.estacion_id,
            "fecha": self.fecha,
            "temperatura": self.temperatura,
            "humedad": self.humedad,
            "viento": self.viento,
            "lluvia": self.lluvia            
        }