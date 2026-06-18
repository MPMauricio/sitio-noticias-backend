// Espera a que todo el documento HTML esté completamente cargado
document.addEventListener("DOMContentLoaded", () => {
  console.log("El archivo app.js se ha enlazado correctamente.");

  // ==========================================================================
  // 1. MONITOREO DE ESTADÍSTICAS (Protegido)
  // ==========================================================================
  const enlaceLeerMas = document.querySelector("article a");

  // El 'if' evita que el código se rompa si la página no tiene este enlace
  if (enlaceLeerMas) {
    enlaceLeerMas.addEventListener("click", (evento) => {
      console.log("Estadística registrada: El usuario hizo clic en leer más.");
    });
  }

  // ==========================================================================
  // 2. VALIDACIÓN AVANZADA DEL FORMULARIO (Protegido)
  // ==========================================================================
  const formulario = document.querySelector("form");
  const alerta = document.getElementById("mensaje-alerta");

  // El 'if' asegura que esto solo corra en las páginas que tengan formulario
  if (formulario && alerta) {
    formulario.addEventListener("submit", function (e) {
      const inputNombre = document.getElementById("nombre");
      const inputCorreo = document.getElementById("correo");

      const nombreVal = inputNombre.value.trim();
      const correoVal = inputCorreo.value.trim();

      // Reiniciar estilos
      inputNombre.style.borderColor = "";
      inputCorreo.style.borderColor = "";
      alerta.style.display = "none";

      // Validación de Nombre Vacío
      if (nombreVal === "") {
        e.preventDefault();
        inputNombre.style.borderColor = "#e53e3e";
        inputNombre.focus();

        alerta.textContent = "⚠️ Por favor, escribe tu nombre completo.";
        alerta.style.backgroundColor = "#fed7d7";
        alerta.style.color = "#c53030";
        alerta.style.display = "block";
        return;
      }

      // Validación de Estructura de Correo
      const estructuraCorreo = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!estructuraCorreo.test(correoVal)) {
        e.preventDefault();
        inputCorreo.style.borderColor = "#e53e3e";
        inputCorreo.focus();

        alerta.textContent =
          "⚠️ Estructura de correo inválida (Falta '@' o dominio).";
        alerta.style.backgroundColor = "#fed7d7";
        alerta.style.color = "#c53030";
        alerta.style.display = "block";
        return;
      }
    });
  }

  // ==========================================================================
  // 3. LÓGICA DEL MODO OSCURO (Universal para todas las páginas)
  // ==========================================================================
  const botonModo = document.getElementById("btn-modo");

  if (botonModo) {
    botonModo.addEventListener("click", function () {
      document.body.classList.toggle("dark-mode");

      if (document.body.classList.contains("dark-mode")) {
        botonModo.textContent = "☀️ Modo Claro";
        botonModo.style.backgroundColor = "#edf2f7";
        botonModo.style.color = "#1a202c";
      } else {
        botonModo.textContent = "🌙 Modo Oscuro";
        botonModo.style.backgroundColor = "#1a365d";
        botonModo.style.color = "white";
      }
    });
  }
}); // Cierre correcto de la función principal DOMContentLoaded
