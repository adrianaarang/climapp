/**
 * Actualiza los elementos visuales del icono (Sol/Luna/Nubes/Lluvia)
 */
function actualizarIconoVisual(data) {
    const container = document.getElementById("weather-icon-container");
    const sun = document.getElementById("sun-icon");

    if (!container || !sun) return;

    // 1. Limpiar nubes o lluvia anteriores
    container.querySelectorAll('.cloud, .rain-drops').forEach(el => el.remove());

    // 2. Resetear clases de estado
    sun.className = "sun"; 

    // 3. Aplicar Noche o Día
    if (data.es_noche) {
        sun.classList.add("is-night");
    }

    // 4. Aplicar Color por Temperatura
    const temp = Math.round(data.temperatura);
    if (temp <= 12) {
        sun.classList.add("temp-cold");
    } else if (temp >= 28) {
        sun.classList.add("temp-hot");
    }

    // 5. Añadir Nubes o Lluvia según datos de AEMET
    if (data.lluvia > 0) {
        crearNube(container, true);
    } else if (data.humedad > 75) {
        crearNube(container, false);
    }
}

/**
 * Crea una nube y opcionalmente gotas de lluvia
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
 * Función principal que pide la ubicación y llama a la API
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

            // Rellenar datos en pantalla
            temperature.textContent = `${Math.round(data.temperatura)}°`;
            humidity.textContent = `${data.humedad}%`;
            wind.textContent = `${data.viento} km/h`;
            rain.textContent = `${data.lluvia} mm`;
            stationName.textContent = data.estacion;
            cityName.textContent = data.ciudad;
            mainTitle.textContent = `${data.ciudad} · Tiempo Real`;
            updatedAt.textContent = `Hora de última actualización: ${data.hora_display}`;

            // Actualizar Icono
            actualizarIconoVisual(data);

            // Estado verde
            statusDot.style.background = "#22c55e";
            statusDot.style.boxShadow = "0 0 12px rgba(34, 197, 94, 0.45)";

        } catch (error) {
            console.error(error);
            updatedAt.textContent = "Error de conexión";
            statusDot.style.background = "#ef4444";
        }
    }, (err) => {
        updatedAt.textContent = "Permiso de ubicación denegado";
    });
}

// Iniciar al cargar la página
document.addEventListener("DOMContentLoaded", () => {
    actualizarClima();

    const refreshBtn = document.getElementById("refreshBtn");
    if (refreshBtn) {
        refreshBtn.addEventListener("click", actualizarClima);
    }
});

            //  24/04 A la espera de intregar con Isabela