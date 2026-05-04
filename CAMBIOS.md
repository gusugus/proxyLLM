## [2026-04-23]
> [!IMPORTANT]
> **REGLA CRÍTICA**: NO modificar la estructura de los prompts en `rules.py` sin petición explícita. El usuario está refinando la redacción manualmente.

### Implementación de Modo Tutor (Preguntas Fallidas)

- **Memoria de Conversación Natural**: Se re-implementó el historial de sesión (últimos 3-4 intercambios) con un nuevo formato descriptivo. El objetivo es que el tutor pueda responder a saludos, agradecimientos y preguntas de seguimiento de forma fluida, manteniendo siempre el contexto de los errores previos.
- **Contexto de Materia**: Soporte para el campo `materia` para ampliar el contexto temático.
- **Mapeo de Datos**: Normalización a `studentAnswer`.
- **Restricción de Conversación**: Se refinó la instrucción para permitir diálogos educativos dentro del tema de la materia, bloqueando solo temas ajenos.
- **Logging de Interacción**: Se registra la interacción completa (Prompt y Respuesta), incluyendo ahora el **proceso de pensamiento (`thought`)** y los tokens individuales en tiempo real.
- **Infraestructura de Chat**: Se añadió soporte para el endpoint `/v1/chat/completions` (OpenAI style) mediante la bandera `USE_CHAT_COMPLETIONS` en `config.py`. Por defecto está desactivada (`false`) para mantener el comportamiento actual que es más fluido.
- **Simplificación del Orquestador**: `chat_orchestrator.py` vuelve a ser puramente un comunicador.

### Refactorización y Cumplimiento de Reglas (60 líneas)

- **División de Responsabilidades**:
  - `proxy/services/rules.py`: Maneja la inyección de reglas y prompts dinámicos.
  - `proxy/services/grammar_service.py`: Gestión de gramática GBNF.
  - `proxy/services/chat_orchestrator.py`: Selección de backend y ejecución.
- **Detección de Keywords**: Refinada para evitar interferencias entre reglas de sistema y mensajes de usuario.

### Refactorización Estructural (Regla 60 líneas)

- **División de `chat.py`**:
  - `proxy/routes/chat.py`: Manejo de rutas y Blueprint.
  - `proxy/services/chat_orchestrator.py`: Lógica de selección de backend.
  - `proxy/services/stream_handler.py`: Generación de eventos SSE.
- **División de `quiz_service.py`**:
  - `proxy/services/quiz_saver.py`: Guardado de JSON en disco.
  - `proxy/services/quiz_uploader.py`: Gestión del proceso background de Node.js.

### Automatización y Genéricos

- **Renombramiento de Servicios**:
  - `quiz_saver.py` $\rightarrow$ `persistence_service.py` (Manejo genérico de archivos JSON).
  - `quiz_uploader.py` $\rightarrow$ `automation_service.py` (Manejo genérico de procesos externos).
- **Abstracción**: Los servicios ya no dependen del concepto de "Quiz" en su nombre o lógica interna, permitiendo su reutilización futura.
- **Actualización de Handlers**: `stream_handler.py` actualizado para usar los nuevos servicios.

### Correcciones y Estabilidad

- Mejora en la carga de `.env` (rutas absolutas y modo override).
- Diagnóstico detallado de errores en el guardado de archivos.
- Limpieza automática de subprocesos al cerrar el proxy (`atexit`).
