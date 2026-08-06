# Metodología

Para practicar un poco el uso de los comandos de **git** mientras aprendemos **Python**/**Typescript**:

1. Creá un fork de este repositorio desde GitHub.
2. Cloná tu versión en tu equipo usando la opción **SSH**. 
   * `git clone git@github.com:Pazitos10/ejercicios-ds.git`
3. En una terminal, ubicate en la carpeta del repositorio y movete a la rama correspondiente:
    * `ejercicios-python`: Para ejercicios de **Python**.
    * `ejercicios-ts`: Para ejercicios de **TypeScript**.
    Recordá que para hacerlo debés utilizar el comando `git checkout <nombre rama>` o `git switch <nombre rama>`
4. Por cada ejercicio, creá una carpeta separada cuyo nombre sea `ejercicio-<num. ejercicio>`. 
5. Utilizá `git status` para ir controlando el estado del **Staging Area**
6. Cuando lo creas indicado, añadí los archivos/directorios al **Staging Area**. `git add <archivos/directorios>`
7. Creá los commits que creas necesarios. `git commit -m "<mensaje descriptivo de los cambios>"`. Utilizá `git log` para monitorear tu avance.
8. Pusheá los cambios a tu versión del repo. `git push -u origin <nombre de la rama en la que estás trabajando>`
9. Cuando estés listo/a, creá un **Pull Request** en la versión [original](https://github.com/Pazitos10/ejercicios-ds/pulls) del proyecto, comparando la rama que modificaste contra la homónima en el proyecto original.

**Observación:** El objetivo no es que esos cambios sean mergeados y formen parte del proyecto original sino simplemente una excusa para permitirnos ganar confianza y fluidez con el uso de git y GitHub.