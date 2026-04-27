/**
 * Gestión del formulario de registro climático.
 * Encapsulado en DOMContentLoaded para evitar errores de carga.
 */
document.addEventListener("DOMContentLoaded", function() {
    
    const formulario = document.getElementById("form-registro");
    const mensajeDiv = document.getElementById("mensaje");

    // Verificación de seguridad: si no encuentra el formulario, avisa en consola
    if (!formulario) {
        console.error("❌ Error: No se encontró el formulario con ID 'form-registro'");
        return;
    }

    formulario.addEventListener("submit", async function(e) {
        // 1. Detener el envío normal para procesarlo con AJAX/Fetch
        e.preventDefault();

        // 2. Captura y conversión de datos
        // Usamos parseFloat para asegurar que los valores sean números en Python
        const datos = {
            estacion_id: document.getElementById("estacion_id").value.trim(),
            fecha:       document.getElementById("fecha").value,
            temperatura: parseFloat(document.getElementById("temperatura").value),
            humedad:     parseFloat(document.getElementById("humedad").value),
            viento:      parseFloat(document.getElementById("viento").value),
            lluvia:      parseFloat(document.getElementById("lluvia").value)
        };

        // 3. Validación de Humedad (Frontend)
        // Evita el envío si el valor no es numérico o está fuera de rango
        const humValue = document.getElementById("humedad").value;
        if (humValue === "" || isNaN(datos.humedad) || datos.humedad < 0 || datos.humedad > 100) {
            mensajeDiv.innerText = "❌ La humedad debe estar entre 0% y 100%";
            mensajeDiv.style.color = "#ef4444";
            return;
        }

        // 4. Feedback visual de carga
        mensajeDiv.innerText = "⏳ Guardando registro...";
        mensajeDiv.style.color = "#3b82f6";

        try {
            // 5. Envío al controlador de Flask
            const response = await fetch('/api/registrar', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(datos)
            });

            const resultado = await response.json();

            if (response.ok) {
                // Éxito total
                mensajeDiv.innerText = "✔ " + (resultado.message || "Guardado con éxito");
                mensajeDiv.style.color = "#22c55e";
                
                // Limpiar campos para el siguiente registro
                formulario.reset();
            } else {
                // El servidor (Python) rechazó los datos por validación
                mensajeDiv.innerText = "❌ " + (resultado.message || "Error en el servidor");
                mensajeDiv.style.color = "#ef4444";
            }

        } catch (error) {
            // Fallo de conexión o error crítico
            mensajeDiv.innerText = "❌ No se pudo conectar con el servidor";
            mensajeDiv.style.color = "#ef4444";
            console.error("Error en Fetch:", error);
        }
    });
});