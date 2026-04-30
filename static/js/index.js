/**
 * Actualiza los elementos visuales del icono (Sol/Luna/Nubes/Lluvia)
 */
function actualizarIconoVisual(data) {
    const container = document.getElementById("weather-icon-container");
    const sun = document.getElementById("sun-icon");

    if (!container || !sun) return;

    // Limpiar iconos anteriores
    container.querySelectorAll('.cloud, .rain-drops').forEach(el => el.remove());

    // Resetear clases
    sun.className = "sun";

    // Noche o día
    if (data.es_noche) {
        sun.classList.add("is-night");
    }

    // Color por temperatura
    const temp = Math.round(data.temperatura);
    if (temp <= 12) {
        sun.classList.add("temp-cold");
    } else if (temp >= 28) {
        sun.classList.add("temp-hot");
    }

    // Nubes o lluvia
    if (data.lluvia > 0) {
        crearNube(container, true);
    } else if (data.humedad > 75) {
        crearNube(container, false);
    }
}

/**
 * Crea nube y lluvia opcional
 */
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
 * Función principal
 */
async function actualizarClima() {
    const temperature = document.getElementById("temperature");
    const humidity = document.getElementById("humidity");
    const wind = document.getElementById("wind");
    const rain = document.getElementById("rain");
    const stationName = document.getElementById("stationName");
    const cityName = document.getElementById("cityName");
    const mainTitle = document.getElementById("mainTitle");
    const updatedAt = document.getElementById("updatedAt");
    const statusDot = document.getElementById("statusDot");

    if (!navigator.geolocation) {
        updatedAt.textContent = "GPS no soportado";
        return;
    }

    updatedAt.textContent = "Localizando...";

    navigator.geolocation.getCurrentPosition(async (position) => {
        const { latitude, longitude } = position.coords;

        try {
            const response = await fetch(`/api/clima?lat=${latitude}&lon=${longitude}`);
            const data = await response.json();

            if (!response.ok) throw new Error(data.error);

            // Rellenar datos
            temperature.textContent = `${Math.round(data.temperatura)}°`;
            humidity.textContent = `${data.humedad}%`;
            wind.textContent = `${data.viento} km/h`;
            rain.textContent = `${data.lluvia} mm`;
            stationName.textContent = data.estacion;
            cityName.textContent = data.ciudad;
            mainTitle.textContent = `${data.ciudad} · Tiempo Real`;

            // 🔥 SOLUCIÓN: usar hora local SIEMPRE
            const horaActual = new Date().toLocaleTimeString("es-ES", {
                hour: "2-digit",
                minute: "2-digit"
            });

            updatedAt.textContent = `Hora de última actualización: ${horaActual}`;

            // Icono
            actualizarIconoVisual(data);

            // Estado OK
            statusDot.style.background = "#22c55e";
            statusDot.style.boxShadow = "0 0 12px rgba(34, 197, 94, 0.45)";

        } catch (error) {
            console.error(error);
            updatedAt.textContent = "Error de conexión";
            statusDot.style.background = "#ef4444";
        }

    }, () => {
        updatedAt.textContent = "Permiso de ubicación denegado";
    });
}

// Inicio
document.addEventListener("DOMContentLoaded", () => {
    actualizarClima();

    const refreshBtn = document.getElementById("refreshBtn");
    if (refreshBtn) {
        refreshBtn.addEventListener("click", actualizarClima);
    }
});