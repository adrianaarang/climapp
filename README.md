<p align="center">
  <img src="https://img.shields.io/badge/ClimApp-B2B_Climate_Resilience-blue?style=for-the-badge&logo=appveyor" alt="Banner">
</p>

# 🌍 ClimApp: Inteligencia Climática de Alta Disponibilidad

> **Business Case:** En un mercado global donde el clima dicta la eficiencia operativa, la falta de datos hiperlocales es un riesgo financiero. **ClimApp** nace como una solución B2B diseñada para **entornos logísticos e industriales de alta precisión**, transformando la incertidumbre climática en activos de decisión mediante un modelo de datos híbrido y trazable.

---

## 💼 Identidad de Producto

| Desafío del Sector | Solución ClimApp |
| :--- | :--- |
| **Zonas de Sombra de Datos** | **Modelo Híbrido:** Combina la precisión masiva de la API de AEMET con la captura manual humana para micro-climas industriales. |
| **Integridad del Dato** | **Validación Estricta:** Implementación de *Guard Clauses* y validación de tipos para evitar la ingesta de ruido o datos corruptos. |
| **Falta de Trazabilidad** | **Telemetría de Auditoría:** Sistema de logs de nivel empresarial que registra el linaje del dato desde la captura hasta el almacenamiento. |

---

## 🏗️ Excelencia Arquitectónica

Hemos implementado una arquitectura de **capas desacopladas** (CSR: Controller-Service-Repository) que garantiza la escalabilidad y facilita el mantenimiento.

### 🛠️ Stack Tecnológico
*   **Core:** Python 3.12+ & Flask (Agilidad y eficiencia en microservicios).
*   **Resiliencia:** Protocolos de *Location Failover* (GPS > Geo-Coding > IP Inferred).
*   **Persistencia:** JSON dinámico para portabilidad total y futura migración a SQL.

---
  
## ⚡ Inicio Rápido (Quick Start)

Sigue estos pasos para desplegar el entorno de desarrollo en menos de 2 minutos:

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/tu-usuario/climapp.git](https://github.com/tu-usuario/climapp.git)
   cd climapp

2. **Configurar el entorno virtual:**
   python -m venv venv
source venv/Scripts/activate  # En Windows: venv\Scripts\activate

3. **Instalar dependencias:**
   pip install -r requirements.txt

4. **Variables de Entorno:**
   Crea un archivo .env en la raíz del proyecto e incluye tu clave de AEMET:
   AEMET_API_KEY=tu_api_key_aqui
   FLASK_ENV=development

5. **Lanzar la aplicación:**
    python app.py

---


### 🗺️ Patrón de Flujo de Datos
```mermaid
graph TD
    A[Capa de Captura: UI/API] -->|Request| B[Controladores: Gateway]
    B -->|Orquestación| C[Servicios: Lógica de Negocio]
    C -->|Normalización| D[Alert Service: Motor de Riesgos]
    D -->|Persistencia| E[Repositorio: Data Lake JSON]
    C -.->|Telemetría| F[Logging Service]
```

---

## 📜 El Contrato de Datos (Single Source of Truth)

Para **Climapp**, la procedencia es tan importante como el valor. Nuestro esquema garantiza que cada registro sea único y auditable.

### 🔍 Diccionario de Datos
*   `id`: Identificador único (UUID v4) para evitar colisiones en la sincronización.
*   `fuente`: Campo crítico de **Data Lineage**. Diferencia si el dato es `Manual` o       `API_AEMET` para análisis de sesgos.
*   `alertas`: Array de riesgos detectados automáticamente por el motor de reglas.

### ⚠️ Protocolos de Seguridad (Umbrales de Alerta)

El sistema evalúa en tiempo real los siguientes límites técnicos para disparar protocolos de seguridad:

| Parámetro | Umbral | Alerta | Acción Sugerida |
| :--- | :--- | :--- | :--- |
| **Temperatura** | **≥ 40.0°C** | 🔴 **ROJA** | Parada operativa por estrés térmico. |
| **Temperatura** | **≥ 35.0°C** | 🟠 **NARANJA** | Hidratación y descansos obligatorios. |
| **Temperatura** | **≤ 0.0°C** | ❄️ **HELADA** | Riesgo en pavimentos y fluidos. |
| **Viento** | **> 70.0 km/h** | 🌪️ **VIENTO** | Asegurar carga y estructuras. |
| **Lluvia** | **> 30.0 mm** | 🌧️ **INTENSA** | Revisión de drenajes y logística. |

---

## 🛠️ Ingeniería de Calidad & Telemetría

### 🧪 QA & Blindaje contra Regresiones
Utilizamos **Pytest** con una cobertura del 100% en las rutas críticas del repositorio. 
*   **Mocking:** Simulamos respuestas de AEMET para testear el comportamiento del sistema en condiciones de red extremas.
*   **Resultados:** Actualmente **7/7 tests PASSED**, garantizando que cada refactorización mantiene la integridad del sistema.

```bash
# Comando de ejecución de auditoría técnica
pytest tests/ -v
```

### 🛰️ Telemetría y Diagnóstico (app.log)
El archivo `logs/app.log` no es solo un registro; es nuestro panel de diagnóstico en producción. Implementamos niveles de severidad (`INFO`, `WARNING`, `ERROR`, `CRITICAL`) para:
*   Detectar fallos en la API Key de AEMET.
*   Monitorear el éxito del *Failover* de ubicación.
*   Auditar quién y cuándo realiza registros manuales.

---

## 👥 Roles y Metodología (GitHub Flow)

El equipo implementó una metodología de trabajo basada en **GitHub Flow**, priorizando la entrega continua mediante ramas de características (*feature branches*) y revisiones de código cruzadas en Pull Requests para asegurar la estabilidad de la rama `main`.

### Organización del Equipo

* **Adriana (Gateway & UX):**
    * Arquitecta de la base del servidor (`app.py`) y navegación.
    * Responsable del `view_controller.py` y la estructura visual base (`index.html`, CSS y JS base).
* **Isabela (Modelado & Gestión Manual):**
    * Lideró el sistema de entrada de datos manual (`registro.html` y `manual_controller.py`).
    * Definió el modelo de negocio en `registro_climatico.py` y las validaciones de usuario.
* **Juan (Motor AEMET, Servicios & QA):**
    * Desarrolló la integración técnica con **AEMET OpenData** (`weather_api_service.py`) y la lógica de geolocalización inteligente.
    * Arquitecto de los servicios core: **Normalización**, **Sistema de Alertas**, **Reintentos (Retry)** y configuración de variables de entorno (`.env`).
* **Elena (Persistencia, Análisis & Logs):**
    * Responsable de la capa de persistencia en JSON (`json_repository.py`) y la visualización del histórico.
    * Implementó el sistema de seguimiento de eventos (`logging_service.py`) y la comparativa de fuentes de datos.

### Gestión de Calidad y Flujo de Trabajo

* **Estrategia de Ramas:** Uso estricto de nomenclaturas `feat/`, `fix/` y `refactor/`.
* **Contrato de Datos:** Definición de un esquema JSON unificado para garantizar la interoperabilidad entre el motor de AEMET (Juan) y el sistema de consulta (Elena).
* **Políticas de Branch Protection:** Requisito de aprobación de revisión y resolución de hilos de discusión antes de cualquier integración en la rama principal.

---

## 🚀 Roadmap de Evolución

- [ ] **Fase 2:** Migración del Repositorio a **SQLite** para gestión de Big Data climático.
- [ ] **Fase 3:** Dashboard analítico con **visualización avanzada** (Gráficos de tendencia y mapas de calor).
- [ ] **Fase 4:** Integración de modelos de **Machine Learning** para predicción de alertas preventivas.

---
<p align="center">
  <b>© 2026 ClimApp - Weather Data Solutions</b><br>
  <i>"Transformando datos atmosféricos en certeza operativa."</i>
</p>
