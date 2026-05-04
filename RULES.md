No es necesario que me expliques a detalle cada cambio, en cambio, lleva una documentacion de los cambios que se han realizado (en el repositorio actual CAMBIOS.md).
No crees y preguntes un plan, sino solamente realiza los cambios
No crees archivos demasiado grandes. Que no pasen de 60 lineas de codigo en un archivo (Por motivos de lectura de LLM que lee un archivo en varias partes). En caso de pasarse de 60 lineas, rompamos esa funcion y hagamos otro archivo.
Al escribir codigo, tengamos en cuenta una arquitectura por capas (tipo MVC), y creemos archivos/funciones que hagan una sola cosa.
Tengamos en cuenta buenas practicas de codificacion, por ejemplo, reutilizacion de codigo.
Manten retrocompatibilidad con los cambios anteriores.
NO MODIFICAR la estructura de los prompts (ej. en rules.py) a menos que se pida explícitamente. El usuario está ajustando la redacción y estructura manualmente.
