# AGENTS.md - Reglas para el Agente

## Comportamiento general
- Saluda al inicio
- Responde en español
- Trabajas en entorno WSL. Las rutas Windows son /mnt/c/... no C:\...
- Directorio de trabajo base: /mnt/c/Users/gusgus/Documents/laboratorios
- Directorio de proyectos: /home/gus/Rahoot/config/quizz

## Archivos y rutas
- Usa rutas COMPLETAS, nunca rutas relativas
- No uses `cd` para moverte entre directorios
- Para acceder a archivos en Windows, usa /mnt/c/...

## Guardar archivos
Cuando el usuario pida guardar algo:
1. Ejecuta `write` con el contenido
2. Responde " Guardado en [ruta]"

NO verifiques con `ls`
NO expliques los pasos
NO muestres tu razonamiento

# Reglas para GENERAR contenido educativo

## Formato de preguntas (si aplica)
Cuando el usuario pida "crea X preguntas con 4 opciones...":

- NO saludes, NO expliques, NO muestres razonamiento
- Formato exacto:
Genera UN JSON válido con esta estructura EXACTA:

{
    "subject": "tema_extraido_del_usuario",
    "questions": [
        {
            "question": "texto de la pregunta",
            "answers": ["opcion a", "opcion b", "opcion c", "opcion d"],
            "solution": 0,
            "cooldown": 5,
            "time": 15
        }
    ]
}

- solution: índice de la respuesta correcta (0, 1, 2 o 3)
- cooldown: segundos entre preguntas (default: 5)
- time: segundos para responder (default: 15)

## Reglas de indices
- solution: 0 = primera opcion (a)
- solution: 1 = segunda opcion (b)
- solution: 2 = tercera opcion (c)
- solution: 3 = cuarta opcion (d)

## Si el usuario no especifica tema
Responde: {"error": "Por favor, especifica el tema. Ejemplo: '2 preguntas sobre Segunda Guerra Mundial'"}

## Nombre del archivo
Formato: `banco_preguntas_[tema]_[DDMMYYYY].json`
Ejemplo: `banco_preguntas_SegundaGuerraMundial_17042026.json`

- Tema: sin espacios, primera letra de cada palabra en mayuscula
- Fecha: dia, mes, año en formato DDMMYYYY (dos digitos cada uno)

## Guardado
Guarda en: `/home/gus/Rahoot/config/quizz/[nombre_del_archivo]`
Responde UNICAMENTE: " Guardado en /home/gus/Rahoot/config/quizz/[nombre_del_archivo]"