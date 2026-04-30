document.addEventListener("DOMContentLoaded", async function () {

    const formulario = document.getElementById("form-registro");
    const municipioInput = document.getElementById("municipio_input");
    const hiddenInput = document.getElementById("estacion_id");
    const datalist = document.getElementById("estaciones_list");
    const mensajeDiv = document.getElementById("mensaje");
    const fechaInput = document.getElementById("fecha");

    let listaMunicipios = [];

    const hoy = new Date().toISOString().split("T")[0];
    fechaInput.setAttribute("max", hoy);

    try {
        const respuesta = await fetch("/static/js/estacion_por_municipio.json");
        const datos = await respuesta.json();

        listaMunicipios = datos.estacion_por_municipio || [];

        listaMunicipios.forEach(function (item) {
            const option = document.createElement("option");
            option.value = item.municipio;
            datalist.appendChild(option);
        });

    } catch (error) {
        console.error("Error cargando municipios:", error);
        mostrarMensaje("Error cargando la lista de municipios", "error");
    }

    municipioInput.addEventListener("input", function () {
        const valorEscrito = municipioInput.value.trim().toLowerCase();

        const seleccion = listaMunicipios.find(function (item) {
            return item.municipio.toLowerCase() === valorEscrito;
        });

        if (seleccion) {
            hiddenInput.value = seleccion.id_estacion;
            municipioInput.style.borderLeft = "4px solid #22c55e";
        } else {
            hiddenInput.value = "";
            municipioInput.style.borderLeft = "3px solid var(--accent)";
        }
    });

    formulario.addEventListener("submit", async function (e) {
        e.preventDefault();

        limpiarMensaje();

        const valorMunicipio = municipioInput.value.trim().toLowerCase();

        const coincidencia = listaMunicipios.find(function (item) {
            return item.municipio.toLowerCase() === valorMunicipio;
        });

        if (coincidencia) {
            hiddenInput.value = coincidencia.id_estacion;
            municipioInput.value = coincidencia.municipio;
        }

        if (!hiddenInput.value) {
            mostrarMensaje("Selecciona un municipio válido de la lista", "error");
            return;
        }

        const fechaRaw = fechaInput.value;
        const temperatura = parseFloat(document.getElementById("temperatura").value);
        const humedad = parseFloat(document.getElementById("humedad").value);
        const viento = parseFloat(document.getElementById("viento").value);
        const lluvia = parseFloat(document.getElementById("lluvia").value);

        if (!fechaRaw) {
            mostrarMensaje("Debes introducir una fecha", "error");
            return;
        }

        if (fechaRaw > hoy) {
            mostrarMensaje("No puedes introducir una fecha posterior al día de hoy", "error");
            return;
        }

        if (isNaN(temperatura) || temperatura < -50 || temperatura > 50) {
            mostrarMensaje("La temperatura debe estar entre -50 ºC y 50 ºC", "error");
            return;
        }

        if (isNaN(humedad) || humedad < 0 || humedad > 100) {
            mostrarMensaje("La humedad debe estar entre 0 y 100%", "error");
            return;
        }

        if (isNaN(viento) || viento < 0) {
            mostrarMensaje("El viento no puede ser negativo", "error");
            return;
        }

        if (isNaN(lluvia) || lluvia < 0) {
            mostrarMensaje("La lluvia no puede ser negativa", "error");
            return;
        }

        const partesFecha = fechaRaw.split("-");
        const year = partesFecha[0];
        const month = partesFecha[1];
        const day = partesFecha[2];

        const fechaLimpia = `${day}/${month}/${year}`;

        const datosEnvio = {
            estacion_id: hiddenInput.value,
            municipio: municipioInput.value,
            fecha: fechaLimpia,
            temperatura: temperatura,
            humedad: humedad,
            viento: viento,
            lluvia: lluvia
        };

        try {
            const response = await fetch("/api/registrar", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(datosEnvio)
            });

            const resultado = await response.json();

            if (response.ok) {
                mostrarMensaje(resultado.message || "Registro guardado correctamente", "success");

                if (resultado.alertas && resultado.alertas.length > 0) {
                    mostrarAlertasClimaticas(resultado.alertas);
                }

                formulario.reset();
                hiddenInput.value = "";
                municipioInput.style.borderLeft = "3px solid var(--accent)";
                fechaInput.setAttribute("max", hoy);

            } else {
                mostrarMensaje(resultado.error || resultado.message || "Error al guardar el registro", "error");
            }

        } catch (error) {
            console.error("Error de conexión:", error);
            mostrarMensaje("Error de conexión con el servidor", "error");
        }
    });

    function limpiarMensaje() {
        mensajeDiv.innerHTML = "";
        mensajeDiv.className = "message";
        mensajeDiv.style.display = "none";
    }

    function mostrarMensaje(texto, tipo) {
        mensajeDiv.innerHTML = "";
        mensajeDiv.style.display = "block";
        mensajeDiv.className = "message";

        const textoMensaje = document.createElement("div");
        textoMensaje.innerText = texto;
        textoMensaje.classList.add("alert");

        if (tipo === "success") {
            textoMensaje.classList.add("alert-success");
        } else {
            textoMensaje.classList.add("alert-error");
        }

        mensajeDiv.appendChild(textoMensaje);
    }

    function mostrarAlertasClimaticas(alertas) {
        const contenedorAlertas = document.createElement("div");
        contenedorAlertas.classList.add("alertas-climaticas");

        alertas.forEach(function (alerta) {
            const alertaDiv = document.createElement("div");

            let mensaje = "";
            let nivel = "verde";

            if (typeof alerta === "string") {
                const alertaMayuscula = alerta.toUpperCase();

                if (alertaMayuscula.includes("ROJA_CALOR")) {
                    nivel = "roja";
                    mensaje = "Alerta roja por calor extremo";

                } else if (alertaMayuscula.includes("NARANJA_CALOR")) {
                    nivel = "naranja";
                    mensaje = "Alerta naranja por temperatura alta";

                } else if (alertaMayuscula.includes("ROJA_FRIO")) {
                    nivel = "roja";
                    mensaje = "Alerta roja por frío extremo";

                } else if (alertaMayuscula.includes("NARANJA_FRIO")) {
                    nivel = "naranja";
                    mensaje = "Alerta naranja por helada";

                } else if (alertaMayuscula.includes("ROJA_VIENTO")) {
                    nivel = "roja";
                    mensaje = "Alerta roja por viento fuerte";

                } else if (alertaMayuscula.includes("NARANJA_VIENTO")) {
                    nivel = "naranja";
                    mensaje = "Alerta naranja por viento moderado";

                } else if (alertaMayuscula.includes("ROJA_LLUVIA")) {
                    nivel = "roja";
                    mensaje = "Alerta roja por lluvia intensa";

                } else if (alertaMayuscula.includes("NARANJA_LLUVIA")) {
                    nivel = "naranja";
                    mensaje = "Alerta naranja por lluvia moderada";

                } else if (alertaMayuscula.includes("NARANJA_HUMEDAD")) {
                    nivel = "naranja";
                    mensaje = "Alerta naranja por humedad alta";

                } else if (alertaMayuscula.includes("VERDE")) {
                    nivel = "verde";
                    mensaje = "Alerta verde: sin riesgo climático";

                } else {
                    nivel = "verde";
                    mensaje = "Alerta verde: sin riesgo climático";
                }

            } else {
                mensaje = alerta.mensaje || "Alerta climática";
                nivel = alerta.nivel || "verde";
            }

            alertaDiv.innerText = mensaje;
            alertaDiv.classList.add("alerta-clima");

            if (nivel === "roja") {
                alertaDiv.classList.add("alerta-roja");
            } else if (nivel === "naranja") {
                alertaDiv.classList.add("alerta-naranja");
            } else {
                alertaDiv.classList.add("alerta-verde");
            }

            contenedorAlertas.appendChild(alertaDiv);
        });

        mensajeDiv.appendChild(contenedorAlertas);
    }

});