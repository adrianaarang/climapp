/**
 * Actualiza los elementos visuales del icono (Sol/Luna/Nubes/Lluvia)
 */
function actualizarIconoVisual(data) {
    const container = document.getElementById("weather-icon-container");
    const sun = document.getElementById("sun-icon");

    if (!container || !sun) return;

    container.querySelectorAll('.cloud, .rain-drops').forEach(el => el.remove());
    sun.className = "sun"; 

    if (data.es_noche) {
        sun.classList.add("is-night");
    }

    const temp = Math.round(data.temperatura);
    if (temp <= 12) {
        sun.classList.add("temp-cold");
    } else if (temp >= 28) {
        sun.classList.add("temp-hot");
    }

    if (data.lluvia > 0) {
        crearNube(container, true);
    } else if (data.humedad > 75) {
        crearNube(container, false);
    }
}

function crearNube(parent, conLluvia) {
    const cloud = document.createElement("div");
    cloud.className = "cloud";
    
    if (conLluvia) {
        const drops = document.createElement("div");
        drops.className = "rain-drops";
        for (let i = 0; i < 3; i++) {
            const d = document.createElement("div");
            d.className = "drop";
            d.style.left = (20 + i * 25) + "px";
            d.style.animationDelay = (i * 0.2) + "s";
            drops.appendChild(d);
        }
        cloud.appendChild(drops);
    }
    parent.appendChild(cloud);
}

/**
 * Función interna para llamar a la API
 */
async function fetchWeatherData(latitude, longitude) {
    const temperature = document.getElementById("temperatura");
    const humidity = document.getElementById("humedad");
    const wind = document.getElementById("viento");
    const rain = document.getElementById("lluvia");
    const stationName = document.getElementById("estacion");
    const cityName = document.getElementById("municipio");
    const mainTitle = document.getElementById("mainTitle");
    const updatedAt = document.getElementById("fecha");
    const statusDot = document.getElementById("statusDot");
    const refreshBtn = document.getElementById("refreshBtn");

    try {
        const response = await fetch(`/api/clima?lat=${latitude}&lon=${longitude}`);
        const data = await response.json();

        if (!response.ok) throw new Error("Error en la respuesta");

        // Rellenar datos numéricos
        temperature.textContent = `${Math.round(data.temperatura)}°`;
        humidity.textContent = `${data.humedad}%`;
        wind.textContent = `${data.viento} km/h`;
        rain.textContent = `${data.lluvia} mm`;
        stationName.textContent = data.estacion;
        cityName.textContent = data.municipio;
        
        // 1. MEJORA DEL TÍTULO: Texto estático y limpio
        if (mainTitle) mainTitle.textContent = "Estado del Clima";

        const fechaActualizacion = new Date(data.fecha);
        updatedAt.textContent = `Actualizado: ${fechaActualizacion.toLocaleTimeString()}`;

        actualizarIconoVisual(data);

        // 2. ÉXITO: Forzamos que el botón vuelva a su estado normal
        statusDot.style.background = "#22c55e";
        statusDot.style.boxShadow = "0 0 12px rgba(34, 197, 94, 0.45)";
        
        if (refreshBtn) {
            refreshBtn.textContent = "Actualizar Datos";
            refreshBtn.style.background = ""; // Quita el rojo si estaba puesto por CSS inline
            refreshBtn.classList.remove("error"); // Quita clases de error si existen
        }

    } catch (error) {
        console.error("Error en la API:", error);
        updatedAt.textContent = "Error al cargar datos";
        statusDot.style.background = "#ef4444";
        if (refreshBtn) {
            refreshBtn.textContent = "Error al actualizar";
            refreshBtn.style.background = "#ef4444";
        }
    }
}

async function actualizarClima() {
    const updatedAt = document.getElementById("fecha");
    if (!navigator.geolocation) {
        updatedAt.textContent = "GPS no soportado";
        return;
    }

    updatedAt.textContent = "Localizando...";

    navigator.geolocation.getCurrentPosition(
        async (position) => {
            fetchWeatherData(position.coords.latitude, position.coords.longitude);
        },
        async (err) => {
            console.warn("GPS denegado. Usando Madrid.");
            fetchWeatherData(40.4167, -3.7033);
        }
    );
}

document.addEventListener("DOMContentLoaded", () => {
    actualizarClima();

    const refreshBtn = document.getElementById("refreshBtn");
    if (refreshBtn) {
        // Usamos onclick para limpiar cualquier basura de eventos anteriores
        refreshBtn.onclick = (e) => {
            e.preventDefault();
            actualizarClima();
        };
    }
});