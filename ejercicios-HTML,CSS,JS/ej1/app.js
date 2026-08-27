const boton = document.getElementById("btn-color");

const colores = ["#ff7675", "#74b9ff", "#55efc4", "#ffeaa7", "#a29bfe", "#fd79a8"];

boton.addEventListener("click", () => {

  const indiceAleatorio = Math.floor(Math.random() * colores.length);
  
  document.body.style.backgroundColor = colores[indiceAleatorio];
});