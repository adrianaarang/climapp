document.addEventListener("DOMContentLoaded", function () {

    const loginForm = document.getElementById("loginForm");
    const registroForm = document.getElementById("registroForm");

    function showError(elementId, message) {
        const errorElement = document.getElementById(elementId);

        if (errorElement) {
            errorElement.textContent = message;
            errorElement.style.color = "#f87171";
            errorElement.style.fontSize = "0.78rem";
        }
    }

    function validateEmail(email) {
        const regexEmail = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return regexEmail.test(email);
    }

    if (loginForm) {
        loginForm.addEventListener("submit", function (e) {
            let valid = true;

            const email = document.getElementById("email").value.trim();
            const password = document.getElementById("password").value.trim();

            showError("emailError", "");
            showError("passwordError", "");

            if (!validateEmail(email)) {
                showError("emailError", "Introduce un correo válido.");
                valid = false;
            }

            if (password.length === 0) {
                showError("passwordError", "La contraseña es obligatoria.");
                valid = false;
            }

            if (!valid) {
                e.preventDefault();
            }
        });
    }

    if (registroForm) {
        registroForm.addEventListener("submit", function (e) {
            let valid = true;

            const email = document.getElementById("email").value.trim();
            const password = document.getElementById("password").value.trim();
            const confirmPassword = document.getElementById("confirm_password").value.trim();

            showError("emailError", "");
            showError("passwordError", "");
            showError("confirmPasswordError", "");

            if (!validateEmail(email)) {
                showError("emailError", "Email no válido. Ejemplo: correo@dominio.com");
                valid = false;
            }

            if (password.length < 6) {
                showError("passwordError", "La contraseña debe tener al menos 6 caracteres.");
                valid = false;
            }

            if (password !== confirmPassword) {
                showError("confirmPasswordError", "Las contraseñas no coinciden.");
                valid = false;
            }

            if (!valid) {
                e.preventDefault();
            }
        });
    }

});