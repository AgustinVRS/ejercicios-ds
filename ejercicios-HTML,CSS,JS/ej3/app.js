// 1. Capturamos los elementos del DOM por sus IDs
const formulario = document.getElementById("formulario");
const inputNombre = document.getElementById("input-nombre");
const inputCorreo = document.getElementById("input-correo");
const mensaje = document.getElementById("mensaje");


formulario.addEventListener("submit", (evento) => {
  evento.preventDefault();


  const nombre = inputNombre.value.trim();
  const correo = inputCorreo.value.trim();

  
  if (nombre === "" || correo === "") {
    mensaje.textContent = "Error: Por favor completá todos los campos.";
    mensaje.className = "error";
  } else {
    mensaje.textContent = `¡Formulario enviado con éxito! Bienvenido, ${nombre}.`;
    mensaje.className = "exito";

    formulario.reset();
  }
});