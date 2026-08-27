// 1. Guardamos las referencias a los elementos del HTML
const inputTarea = document.getElementById("input-tarea");
const btnAgregar = document.getElementById("btn-agregar");
const listaTareas = document.getElementById("lista-tareas");

// 2. Función que maneja la lógica de creación y borrado
function agregarTarea() {
  const texto = inputTarea.value.trim();

  // Validación para evitar agregar ítems vacíos
  if (texto === "") {
    alert("Por favor, ingresá una tarea.");
    return;
  }

  // Creamos el nuevo <li> y le asignamos el texto
  const nuevaTarea = document.createElement("li");
  nuevaTarea.textContent = texto;

  // Escuchador para borrar el elemento al hacerle clic
  nuevaTarea.addEventListener("click", () => {
    nuevaTarea.remove();
  });

  // Agregamos el elemento a la lista <ul>
  listaTareas.appendChild(nuevaTarea);

  // Limpiamos el campo y volvemos a hacer foco en él
  inputTarea.value = "";
  inputTarea.focus();
}

// 3. Escuchamos el clic en el botón
btnAgregar.addEventListener("click", agregarTarea);

// 4. Permitimos agregar también presionando la tecla Enter
inputTarea.addEventListener("keydown", (e) => {
  if (e.key === "Enter") {
    agregarTarea();
  }
});