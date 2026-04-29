# 🌦️ ClimApp

### Aplicación web para consultar, registrar y comparar datos meteorológicos en España

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Flask](https://img.shields.io/badge/Flask-Web%20App-black)
![AEMET](https://img.shields.io/badge/API-AEMET-red)
![Estado](https://img.shields.io/badge/Estado-En%20desarrollo-success)

---

## 📌 Descripción

**ClimApp** es una aplicación web desarrollada con **Python + Flask** que permite consultar el tiempo en España en tiempo real utilizando la **API oficial de AEMET**.

La aplicación detecta la ubicación del usuario mediante GPS, localiza la estación meteorológica AEMET más cercana y muestra datos actualizados de:

- Temperatura  
- Humedad  
- Viento  
- Presión atmosférica  
- Precipitaciones  
- Alertas meteorológicas  

Además, permite registrar datos climáticos manuales, consultar históricos y comparar las mediciones introducidas por el usuario con los datos oficiales de AEMET.

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

## 📝 Registro manual de datos climáticos

Desde /registro, el usuario puede introducir sus propias mediciones:

Fecha
Temperatura
Humedad
Velocidad del viento
Lluvia
Municipio
Estación AEMET asociada

Los datos se validan y se almacenan localmente en formato JSON.
''

## 📂 Consulta de histórico

Desde /consulta, se pueden filtrar registros guardados por:

- Municipio
- Fecha

## 🔍 Comparación con AEMET

Desde /comparar, ClimApp permite comparar un registro manual con los datos oficiales de AEMET.

Se calculan diferencias en:

- Temperatura
- Humedad
- Viento
- Lluvia

## 🚨 Sistema de alertas
Alerta	Condición
ROJA	Temperatura ≥ 40 ºC
NARANJA	Temperatura ≥ 35 ºC
HELADA	Temperatura ≤ 0 ºC
VIENTO_FUERTE	Viento > 70 km/h
LLUVIA_INTENSA	Lluvia > 30 mm
HUMEDAD_ALTA	Humedad ≥ 90%

## 🏗️ Arquitectura

El proyecto utiliza un patrón de diseño desacoplado para separar la lógica de negocio de la interfaz:

**Templates** ↔ **Controllers** ➔ **Services** ➔ **Repositories** ➔ **Models**

---

### 📂 Estructura de Capas

* **🎨 Templates (Vistas)**
    * `index.html`
    * `dashboard.html`
    * `alerts.html`
* **🎮 Controllers** (Gestión de flujo)
    * `view_controller.py`
    * `manual_controller.py`
    * `compare_controller.py`
* **⚙️ Services** (Lógica y APIs)
    * `WeatherAPIService`
    * `NormalizerService`
    * `AlertService`
    * `RetryService`
* **📦 Repositories** (Datos)
    * `JSONRepository`
* **🏛️ Models** (Entidades)
    * `RegistroClimatico`
    * `Zona`

## 🔄 Flujo de Datos en Tiempo Real

Para procesar la información climática, el sistema sigue este flujo:

1. **Usuario:** Permite acceso a la ubicación.
2. **Frontend:** Obtiene coordenadas ($lat, lon$).
3. **Backend:** Recibe petición en `GET /api/clima`.
4. **API AEMET:** Se consulta el endpoint oficial.
5. **Procesamiento:** * Selección de la estación más cercana.
   * Normalización de datos.
   * Evaluación de alertas climáticas.
6. **Respuesta:** Envío de JSON al navegador para actualizar la interfaz.

---

## 🔌 Integración con AEMET

ClimApp utiliza el OpenData de AEMET. La API funciona mediante un sistema de **doble petición**:

1. **Petición inicial:** Se solicita el recurso al endpoint de observación convencional.
2. **Datos:** AEMET responde con un JSON que contiene una **URL temporal**.
3. **Descarga:** El sistema realiza una segunda petición a esa URL para obtener los datos climáticos reales.

---

## 🛠️ Tecnologías Utilizadas

| Tecnología | Uso |
| :--- | :--- |
| **Python** | Lenguaje principal del backend |
| **Flask** | Framework web y enrutamiento |
| **Jinja2** | Renderizado de plantillas dinámicas |
| **JavaScript** | Gestión de geolocalización y Fetch API |
| **Requests** | Consumo de la API externa de AEMET |
| **Pytest** | Suite de pruebas unitarias |
| **JSON** | Sistema de persistencia de datos |

---

## 📡 Rutas Principales (API & Web)

| Método | Ruta | Descripción |
| :--- | :--- | :--- |
| `GET` | `/` | Dashboard principal |
| `GET` | `/registro` | Formulario de entrada manual |
| `POST` | `/api/registrar` | Persistencia de nuevos datos |
| `GET/POST` | `/consulta` | Visualización del histórico |
| `GET/POST` | `/comparar` | Módulo de comparación climática |
| `GET` | `/api/clima` | Obtención de datos en tiempo real (AEMET) |

---


## ⚙️ Instalación y Configuración

Sigue estos pasos para poner en marcha el proyecto en tu entorno local:

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Configurar variables de entorno

Crea un archivo .env en la raíz del proyecto y añade tus credenciales:

```bash
AEMET_API_KEY=tu_api_key_aqui
SECRET_KEY=tu_clave_secreta
```

### 3. Ejecutar la aplicación
python app.py

```bash
📍 Accede desde tu navegador a:
http://localhost:5000
```
---

### 🧪 Testing y Validación
Para asegurar la integridad de los datos, el sistema aplica las siguientes reglas de negocio:

- Temperatura: rango permitido de -50 a 60 ºC
- Humedad: valores entre 0% y 100%
- Viento / Lluvia: solo valores positivos (≥ 0)

Ejecuta la suite de pruebas unitarias con:

```bash
pytest
```

---

## 🔮 Roadmap

Próximas funcionalidades planeadas para el desarrollo de **ClimApp**:

- [ ] **Persistencia:** Migración a base de datos relacional (PostgreSQL).
- [ ] **Seguridad:** Sistema de autenticación de usuarios (Login/Registro).
- [ ] **Visualización:** Dashboard interactivo con gráficos dinámicos (Chart.js).
- [ ] **Inteligencia:** Implementación de modelos de IA para predicción de tendencias.

---

## 👩‍💻 Autores

| Miembro | Rol | Contacto |
| :--- | :--- | :--- |
| **Adriana Aránguez** | Scrum Master | [@adrianaarang](https://github.com/adrianaarang) |
| **Juan Manuela de la Fuente** | Product Manager | [@juandelaf1](https://github.com/juandelaf1) |
| **Isabela Tellez** | Desarrolladora | [@Isabela-Tellez](https://github.com/Isabela-Tellez) |
| **Elena Carino** | Desarrolladora | [@elenacarino-max](https://github.com/elenacarino-max) |
