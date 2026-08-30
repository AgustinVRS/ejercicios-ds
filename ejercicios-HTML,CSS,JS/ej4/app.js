// 1. Variable para llevar el estado del número
let contador = 0;

// 2. Capturamos los elementos del DOM por sus IDs
const valorContador = document.getElementById("contador");
const btnAumentar = document.getElementById("btn-aumentar");
const btnDisminuir = document.getElementById("btn-disminuir");

// 3. Evento para incrementar el número
btnAumentar.addEventListener("click", () => {
  contador++;
  valorContador.textContent = contador;
});

// 4. Evento para decrementar el número
btnDisminuir.addEventListener("click", () => {
  contador--;
  valorContador.textContent = contador;
});