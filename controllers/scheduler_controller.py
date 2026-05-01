from flask_apscheduler import APScheduler
from services.weather_api_service import obtener_clima_por_coordenadas
from services.normalizer_service import normalizar_datos_aemet
from repositories.json_repository import JSONRepository
import logging

# Instanciamos el scheduler
scheduler = APScheduler()
repo = JSONRepository('data/registros_climaticos.json')

def tarea_actualizar_clima():
    """
    Tarea que se ejecuta automáticamente. 
    Descarga el clima de una estación principal (ej. Madrid Retiro) y lo guarda.
    """
    try:
        # 1. Coordenadas de Madrid por defecto para el histórico automático
        lat, lon = "40.4167", "-3.7033"
        
        # 2. Obtener y normalizar
        raw_data = obtener_clima_por_coordenadas(lat, lon)
        data = normalizar_datos_aemet(raw_data)
        
        # 3. Añadir fuente para saber que fue automático
        data["fuente"] = "automatico"
        
        # 4. Guardar en el JSON
        repo.guardar(data)
        
        print(f"✅ Tarea automática completada: Datos guardados para {data.get('ciudad')}")
        
    except Exception as e:
        logging.error(f"❌ Error en la tarea automática: {e}")

def init_scheduler(app):
    """
    Configura e inicia el programador de tareas
    """
    # Configuración básica
    app.config['SCHEDULER_API_ENABLED'] = True
    
    scheduler.init_app(app)
    
    # Programamos la tarea: cada 2h
    scheduler.add_job(
        id='job_clima_auto', 
        func=tarea_actualizar_clima, 
        trigger='interval', 
        minutes=120
    )
    
    scheduler.start()