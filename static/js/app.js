document.addEventListener("DOMContentLoaded", async function() {
    
    // 1. Referencias al DOM
    const formulario = document.getElementById("form-registro");
    const municipioInput = document.getElementById("municipio_input");
    const hiddenInput = document.getElementById("estacion_id");
    const datalist = document.getElementById("estaciones_list");
    const mensajeDiv = document.getElementById("mensaje");

    let listaMunicipios = [];

    // 2. CARGAR EL ARCHIVO JSON
    try {
        const respuesta = await fetch('/static/js/estacion_por_municipio.json');
        const datos = await respuesta.json();
        listaMunicipios = datos.estacion_por_municipio;

        // 3. POBLAR EL DATALIST (Esto da la predicción)
        listaMunicipios.forEach(item => {
            const option = document.createElement("option");
            option.value = item.municipio;
            datalist.appendChild(option);
        });
        
        console.log("✅ Municipios cargados");

    } catch (error) {
        console.error("❌ Error cargando municipios:", error);
    }

    // 4. LOGICA DE SINCRONIZACIÓN (MEJORADA: Ahora acepta minúsculas)
    municipioInput.addEventListener("input", function() {
        const valorEscrito = this.value.trim().toLowerCase();
        
        // Buscamos ignorando mayúsculas/minúsculas
        const seleccion = listaMunicipios.find(e => e.municipio.toLowerCase() === valorEscrito);
        
        if (seleccion) {
            hiddenInput.value = seleccion.id_estacion;
            this.style.borderLeft = "4px solid #10b981"; // success color
        } else {
            hiddenInput.value = "";
            this.style.borderLeft = "1px solid #ccc";
        }
    });

    // 5. ENVÍO DEL FORMULARIO
    formulario.addEventListener("submit", async function(e) {
        e.preventDefault();

        const valorFinal = municipioInput.value.trim().toLowerCase();
        // Intentamos una última búsqueda por si el usuario escribió rápido y no saltó el 'input'
        const coincidenciaFinal = listaMunicipios.find(e => e.municipio.toLowerCase() === valorFinal);

        if (coincidenciaFinal) {
            hiddenInput.value = coincidenciaFinal.id_estacion;
            // Corregimos el nombre visual para que sea bonito (Ej: Madrid)
            municipioInput.value = coincidenciaFinal.municipio;
        }

        // Si después de intentar corregirlo sigue sin ID, entonces sí damos error
        if (!hiddenInput.value) {
            mensajeDiv.innerText = "❌ Selecciona un municipio válido (ej: Madrid, Valdemorillo...)";
            mensajeDiv.style.color = "#ef4444";
            return;
        }

        // --- PROCESO DE FECHA ---
        const fechaRaw = document.getElementById("fecha").value; 
        if (!fechaRaw) {
            mensajeDiv.innerText = "❌ Selecciona una fecha";
            return;
        }
        const [year, month, day] = fechaRaw.split("-");
        const fechaLimpia = `${day}/${month}/${year}`; 

        const datosEnvio = {
            estacion_id: hiddenInput.value,
            municipio:   municipioInput.value, 
            fecha:       fechaLimpia,
            temperatura: parseFloat(document.getElementById("temperatura").value),
            humedad:     parseFloat(document.getElementById("humedad").value),
            viento:      parseFloat(document.getElementById("viento").value),
            lluvia:      parseFloat(document.getElementById("lluvia").value)
        };

        try {
            const response = await fetch('/api/registrar', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(datosEnvio)
            });

            const resultado = await response.json();

            if (response.ok) {
                mensajeDiv.innerText = "✔ Registro guardado correctamente";
                mensajeDiv.style.color = "#10b981";
                formulario.reset();
                hiddenInput.value = "";
                municipioInput.style.borderLeft = "1px solid #ccc";
            } else {
                mensajeDiv.innerText = "❌ " + (resultado.message || "Error al guardar");
                mensajeDiv.style.color = "#ef4444";
            }
        } catch (error) {
            mensajeDiv.innerText = "❌ Error al conectar con el servidor";
            mensajeDiv.style.color = "#ef4444";
        }
    });
});