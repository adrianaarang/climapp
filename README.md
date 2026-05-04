
# 🌦️ ClimApp

### Aplicación web para consultar, registrar y comparar datos meteorológicos en España

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Flask](https://img.shields.io/badge/Flask-Web%20App-black)
![AEMET](https://img.shields.io/badge/API-AEMET-red)
![Estado](https://img.shields.io/badge/Estado-En%20desarrollo-success)

## 📌 Descripción

**ClimApp** es una robusta aplicación web desarrollada con **Python + Flask** diseñada para la monitorización climática precisa en España, integrando directamente la **API oficial de AEMET OpenData**.

El núcleo de la aplicación reside en su capacidad de geolocalización inteligente: detecta la ubicación del usuario mediante GPS, calcula mediante algoritmos geoespaciales la estación meteorológica oficial más cercana y sirve datos en tiempo real sobre:

*   🌡️ **Temperatura** (gestión de máximas y mínimas).
*   💧 **Humedad** relativa del aire.
*   💨 **Viento** (velocidad y dirección).
*   🎈 **Presión atmosférica**.
*   🌧️ **Precipitaciones** acumuladas.
*   ⚠️ **Alertas meteorológicas** críticas.

Más allá de la consulta, **ClimApp** ofrece herramientas avanzadas de gestión de datos que permiten **registrar mediciones manuales**, explorar **archivos históricos** y realizar una **auditoría comparativa** entre los registros del usuario y los estándares oficiales de AEMET.

---
## 📺 Demo del Proyecto

Puedes ver el funcionamiento de **ClimApp** (geolocalización, consulta en tiempo real y registro de datos) en el siguiente video:

https://github.com/user-attachments/assets/561f2d58-f25d-440a-b26f-42ac65f63c47

---


## 📚 Documentación completa

👉 https://mintlify.wiki/adrianaarang/climapp

---

## 🚀 Funcionalidades principales

### 🌍 Consulta meteorológica en tiempo real

ClimApp utiliza la geolocalización del navegador para obtener la latitud y longitud del usuario y enviarlas al endpoint:

```text
GET /api/clima?lat=&lon=
```

A partir de esas coordenadas, la aplicación calcula la estación AEMET más cercana mediante la fórmula de Haversine.

## 📝 Registro Manual de Datos Climáticos

La plataforma permite la entrada de datos propios a través de la ruta `/registro`. Esta funcionalidad está diseñada para usuarios que disponen de estaciones meteorológicas domésticas y desean integrar sus mediciones en el sistema.

### Parámetros de entrada:
*   **Fecha:** Momento exacto de la medición.
*   **Municipio & Estación AEMET:** Selección de la ubicación y vinculación con la estación oficial más cercana para futuras comparativas.
*   **Variables Meteorológicas:** Temperatura, Humedad, Velocidad del viento y Lluvia.

### Validación y Persistencia:
Antes de ser almacenados, los datos pasan por el **`validators.py`** (capa de `utils`) para asegurar que cumplen con los rangos lógicos de negocio. Una vez validados, se guardan localmente en:
1.  **Formato JSON:** En la carpeta `/data` para portabilidad.
2.  **Base de Datos:** Registro en el histórico de `clima.db` a través de los repositorios.
## 📂 Consulta de Histórico

El sistema permite auditar y revisar todos los datos almacenados a través de la ruta `/consulta`. Esta interfaz interactúa directamente con el `JSONRepository` y el `SQLiteRepository` para recuperar la información persistida.

Los registros pueden ser filtrados mediante los siguientes criterios:

*   **Municipio:** Localización específica de la toma de datos (basado en el catálogo de `municipios.json`).
*   **Fecha:** Búsqueda cronológica para analizar la evolución climática en días específicos.

> **Funcionalidad:** Los resultados se presentan en una tabla dinámica que permite una lectura rápida de los parámetros meteorológicos históricos y las alertas que se activaron en su momento.

## 🔍 Comparación con AEMET

Desde el módulo `/comparar`, ClimApp permite realizar una auditoría de datos comparando un **registro manual** (introducido por el usuario) frente a los **datos oficiales** obtenidos en tiempo real de AEMET.

Esta funcionalidad es gestionada por el `compare_controller.py` y permite visualizar desviaciones en:

*   **Temperatura:** Diferencial térmico en grados Celsius (°C).
*   **Humedad:** Variación en el porcentaje de saturación (%).
*   **Viento:** Discrepancia en la velocidad detectada (km/h).
*   **Lluvia:** Diferencia en la precipitación acumulada (mm).

> **Propósito:** Esta herramienta es clave para validar la precisión de estaciones meteorológicas domésticas o registros manuales frente a los sensores de precisión de la red oficial.

## 🚨 Sistema de alertas
| Alerta | Condición |
| :--- | :--- |
| **🔴 ROJA** | Temperatura ≥ 40 ºC |
| **🟠 NARANJA** | Temperatura ≥ 35 ºC |
| **❄️ HELADA** | Temperatura ≤ 0 ºC |
| **💨 VIENTO FUERTE** | Viento > 70 km/h |
| **🌧️ LLUVIA INTENSA** | Lluvia > 30 mm |
| **💧 HUMEDAD ALTA** | Humedad ≥ 90% |

---

## 📂 Estructura del Proyecto

Organización detallada de los componentes del sistema:
```text
.
├── app.py                   # Punto de entrada de la aplicación
├── clima.db                 # Base de datos SQLite local
├── requirements.txt         # Dependencias del proyecto
├── config/                  # ⚙️ Archivos de configuración (JSON)
├── controllers/             # 🎮 Controladores (Lógica de flujo y rutas)
├── data/                    # 📂 Persistencia física (JSON)
├── logs/                    # 📝 Logs de ejecución y errores
├── models/                  # 📦 Entidades de datos (Clases Python)
├── repositories/            # 🗄️ Capa de acceso a datos (JSON/SQLite)
├── services/                # 🚀 Servicios de lógica de negocio y APIs
├── static/                  # ✨ Recursos estáticos (CSS, JS)
├── templates/               # 🎨 Plantillas de vista (HTML)
├── tests/                   # 🧪 Suite de pruebas unitarias y de integración
└── utils/                   # 🛠️ Utilidades, validadores y helpers

```

---
## 🏗️ Arquitectura de Capas

El sistema sigue un patrón de diseño por capas para asegurar la escalabilidad y facilitar el mantenimiento:

### 🎨 Templates (Capa de Presentación)
Contiene las interfaces de usuario desarrolladas en HTML.
* **Vistas principales:** `index.html`, `comparar.html`, `consulta.html`.
* **Vistas de sistema:** `login.html`, `registro.html`, `api.html`.

### 🎮 Controllers (Gestión de Flujo)
Intermediarios que procesan las peticiones y coordinan la lógica entre la vista y los servicios.
* `view_controller.py`: Maneja el renderizado y navegación.
* `auth_controller.py`: Controla la autenticación y sesiones.
* `api_controller.py` & `scheduler_controller.py`: Gestionan endpoints y tareas programadas.

### ⚙️ Services (Lógica de Negocio)
Capas de "inteligencia" que procesan datos y conectan con el exterior.
* **WeatherAPIService**: Integración con APIs climáticas externas.
* **NormalizerService**: Estandarización y limpieza de datos recibidos.
* **AlertService**: Lógica para el disparo de notificaciones.
* **RetryService**: Estrategias de reintento para estabilidad de red.

### 🗄️ Repositories (Acceso a Datos)
Abstracción de la persistencia, permitiendo el uso de múltiples fuentes de datos.
* `sqlite_repository.py`: Gestión de la base de datos relacional (`clima.db`).
* `json_repository.py`: Manejo de archivos planos en `/data` (usuarios y registros).

### 📦 Models (Entidades)
Definición de las estructuras de datos que viajan entre capas.
* `usuario.py`, `registro_climatico.py`, `zona.py`.

### 🛠️ Utils (Utilidades)
Herramientas transversales de apoyo.
* `validators.py`: Validación de formularios y datos.
* `datetime_utils.py`: Formateo y lógica temporal.
* `helpers.py`: Funciones auxiliares genéricas.

### 🧪 Tests (Aseguramiento de Calidad)
Suite de pruebas automatizadas con **Pytest** para validar servicios, controladores y repositorios.

## 🔄 Flujo de Datos en Tiempo Real

Para procesar la información climática, el sistema sigue este flujo de trabajo coordinado entre capas:

1. **Usuario:** Interactúa con la interfaz y permite el acceso a su ubicación geográfica.
2. **Frontend (`app.js`):** Captura las coordenadas ($lat, lon$) mediante la API del navegador y lanza una petición asíncrona al servidor.
3. **Backend (`api_controller.py`):** Recibe la petición en el endpoint `GET /api/clima` y valida los parámetros de entrada.
4. **Consumo de API (`weather_api_service.py`):** Se conecta con el endpoint oficial de AEMET (u otros proveedores) para obtener los datos meteorológicos en bruto.
5. **Procesamiento y Lógica de Negocio:**
   * **Normalización (`normalizer_service.py`):** Transforma la respuesta de la API externa al formato estándar definido en el modelo `RegistroClimatico`.
   * **Evaluación (`alert_service.py`):** Analiza los datos normalizados para detectar umbrales de riesgo y generar alertas si es necesario.
   * **Persistencia (`repositories`):** El sistema guarda una copia del registro procesado en `clima.db` (SQLite) o `registros_climaticos.json` para el histórico.
6. **Respuesta:** El controlador envía el objeto **JSON** final al frontend, que actualiza la interfaz de usuario dinámicamente sin necesidad de recargar la página.

---

## 🔌 Integración con AEMET OpenData

ClimApp consume datos meteorológicos oficiales. La API de AEMET opera bajo un modelo de **doble petición (Handshake)**, el cual hemos implementado de la siguiente manera:

1. **Solicitud de Recurso:** El `WeatherAPIService` envía una petición autenticada con API Key al endpoint de observación.
2. **Generación de Enlace:** AEMET procesa la consulta y responde con un JSON que contiene un "estado" y una **URL temporal de descarga** (válida por pocos minutos).
3. **Descarga de Datos (Payload):** El sistema realiza automáticamente una segunda petición `GET` a esa URL específica para obtener los datos climáticos reales en formato JSON.
4. **Resiliencia:** Debido a la naturaleza de esta doble petición, el **`RetryService`** gestiona posibles cortes de conexión o latencias en la generación del enlace temporal, asegurando que la información llegue siempre al frontend.
---

## 🛠️ Tecnologías Utilizadas

| Tecnología | Uso |
| :--- | :--- |
| **Python 3.13+** | Lenguaje principal del backend y lógica de negocio. |
| **Flask** | Framework web para la gestión de rutas y controladores. |
| **SQLite** | Base de datos relacional para persistencia de usuarios y registros. |
| **JSON** | Formato de intercambio de datos y persistencia secundaria. |
| **Jinja2** | Motor de plantillas para renderizado dinámico de vistas HTML. |
| **JavaScript (ES6+)** | Gestión de geolocalización, Fetch API y manipulación del DOM. |
| **CSS3** | Diseño responsivo y estilos personalizados de la interfaz. |
| **Requests** | Cliente HTTP para el consumo de la API de AEMET OpenData. |
| **Pytest** | Suite de pruebas automatizadas y aseguramiento de calidad. |

---

## 📡 Rutas Principales (API & Web)

| Método | Ruta | Capa | Descripción |
| :--- | :--- | :--- | :--- |
| `GET` | `/` | Vista | Dashboard principal con resumen climatológico. |
| `GET` | `/login` | Vista | Formulario de acceso al sistema. |
| `GET` | `/registro` | Vista | Formulario para entrada manual de datos. |
| `POST` | `/api/registrar` | API | Persistencia de nuevos datos en JSON/SQLite. (En desarrollo) |
| `GET/POST` | `/consulta` | Vista/API | Visualización y filtrado del histórico de registros. |
| `GET/POST` | `/comparar` | Vista/API | Módulo de comparación entre diferentes zonas o fechas. |
| `GET` | `/api/clima` | API | Obtención y normalización de datos en tiempo real (AEMET). |
| `GET` | `/api` | Vista | Documentación o panel de control de la API. |

---


## ⚙️ Instalación y Configuración

Sigue estos pasos para poner en marcha el proyecto en tu entorno local:

### 1. Clonar el repositorio y preparar el entorno
```bash
# Clonar el proyecto
git clone [https://github.com/tu-usuario/climapp.git](https://github.com/tu-usuario/climapp.git)
cd climapp

# Crear e iniciar entorno virtual (Opcional pero recomendado)
python -m venv venv
# En Windows: .\venv\Scripts\activate | En Linux/Mac: source venv/bin/activate
```

---

### 2. Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto y añade tus credenciales. Este archivo es fundamental para que la conexión con la API de AEMET y la seguridad de las sesiones funcionen:

```env
AEMET_API_KEY=tu_api_key_aqui
SECRET_KEY=tu_clave_secreta_personalizada
```
Nota: Consigue tu clave de acceso gratuita en el portal oficial AEMET OpenData.

### 3. Ejecutar la aplicación
Una vez instaladas las dependencias y configuradas las claves, inicia el servidor de desarrollo ejecutando el archivo principal:

```bash
python app.py
```
📍 Acceso local: Abre tu navegador y accede a la siguiente dirección:
```bash
http://localhost:5000
```
---
### 🧪 Testing y Validación

Para asegurar la integridad de los datos y la estabilidad del sistema, se aplica una suite de pruebas automatizadas con **Pytest**. El sistema valida estrictamente las siguientes reglas de negocio antes de permitir cualquier persistencia:

*   **Temperatura:** Rango permitido entre -50 y 60 °C.
*   **Humedad:** Valores porcentuales entre 0% y 100%.
*   **Viento / Lluvia:** Solo se admiten valores positivos ($\geq 0$).
*   **Integridad:** Validación de tipos de datos y obligatoriedad de campos clave (fecha, municipio).

Para ejecutar los tests manualmente y verificar la salud del proyecto:
```bash
pytest -v
```
---

## 🔮 Roadmap

Próximas funcionalidades planeadas para la evolución de **ClimApp**:

- [ ] **Persistencia Avanzada:** Migración completa de archivos JSON a una base de datos relacional robusta (**PostgreSQL**) para entornos de producción.
- [ ] **Visualización de Datos:** Implementación de un dashboard interactivo con gráficos dinámicos utilizando **Chart.js** para analizar tendencias históricas.
- [ ] **Inteligencia Artificial:** Integración de modelos predictivos para anticipar cambios bruscos de temperatura o alertas basadas en datos históricos.
- [ ] **Exportación:** Funcionalidad para descargar reportes climáticos en formato PDF y Excel.

---

## 👩‍💻 Autores

| Miembro | Rol | Contacto |
| :--- | :--- | :--- |
| **Adriana Aránguez** | Scrum Master | [@adrianaarang](https://github.com/adrianaarang) |
| **Juan Manuela de la Fuente** | Product Manager | [@juandelaf1](https://github.com/juandelaf1) |
| **Isabela Tellez** | Desarrolladora | [@Isabela-Tellez](https://github.com/Isabela-Tellez) |
| **Elena Carino** | Desarrolladora | [@elenacarino-max](https://github.com/elenacarino-max) |
