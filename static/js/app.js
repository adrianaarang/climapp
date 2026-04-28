document.addEventListener("DOMContentLoaded", async function() {
    
    // 1. Referencias al DOM
    const formulario = document.getElementById("form-registro");
    const municipioInput = document.getElementById("municipio_input");
    const hiddenInput = document.getElementById("estacion_id");
    const datalist = document.getElementById("estaciones_list");
    const mensajeDiv = document.getElementById("mensaje");

    let listaMunicipios = [];

    // 2. CARGAR EL ARCHIVO JSON (IMPORTANTE)
    try {
        // Ajusta la ruta si tu archivo está en otra carpeta de 'static'
        const respuesta = await fetch('/static/js/estacion_por_municipio.json');
        const datos = await respuesta.json();
        
        // Guardamos el array interno en nuestra variable
        listaMunicipios = datos.estacion_por_municipio;

        // 3. POBLAR EL DATALIST (Autocompletado)
        listaMunicipios.forEach(item => {
            const option = document.createElement("option");
            option.value = item.municipio;
            datalist.appendChild(option);
        });
        
        console.log("✅ Municipios cargados desde el JSON");

    } catch (error) {
        console.error("❌ Error cargando el archivo JSON:", error);
    }

    // 4. LOGICA DE SINCRONIZACIÓN (Nombre -> ID)
    municipioInput.addEventListener("input", function() {
        const seleccion = listaMunicipios.find(e => e.municipio === this.value);
        
        if (seleccion) {
            hiddenInput.value = seleccion.id_estacion;
            this.style.borderLeft = "4px solid var(--success)";
        } else {
            hiddenInput.value = "";
            this.style.borderLeft = "1px solid var(--border)";
        }
    });

    // 5. ENVÍO DEL FORMULARIO
    formulario.addEventListener("submit", async function(e) {
        e.preventDefault();

        if (!hiddenInput.value) {
            mensajeDiv.innerText = "❌ Selecciona un municipio de la lista";
            mensajeDiv.style.color = "#ef4444";
            return;
        }

        const datosEnvio = {
            estacion_id: hiddenInput.value,
            fecha:       document.getElementById("fecha").value,
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
                mensajeDiv.style.color = "var(--success)";
                formulario.reset();
                hiddenInput.value = "";
                municipioInput.style.borderLeft = "1px solid var(--border)";
            }
        } catch (error) {
            mensajeDiv.innerText = "❌ Error al conectar con el servidor";
        }
    });
});