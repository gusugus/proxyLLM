# 📁 ÍNDICE DEL PROYECTO — EduProxy

> Referencia rápida de todos los archivos del proyecto, su capa y su función.

---

## 🟢 Raíz del proyecto

| Archivo | Función |
|---------|---------|
| [app.py](./app.py) | Punto de entrada de Flask. Crea la app, activa CORS y registra los Blueprints. |
| [config.py](./config.py) | Carga las variables de `.env` y las expone como constantes globales (`LLAMACPP_URL`, `AUTO_APPROVE`, etc.). |
| [requirements.txt](./requirements.txt) | Lista de dependencias de Python del proyecto. |
| [.env](./.env) | Variables de entorno locales (URLs, rutas, comandos). **No se sube al repo.** |
| [.gitignore](./.gitignore) | Archivos y carpetas excluidos del control de versiones. |
| [json_quiz.gbnf](./json_quiz.gbnf) | Gramática GBNF que fuerza a llama.cpp a generar JSON con el formato exacto del quiz. |
| [agents.md](./agents.md) | Reglas del sistema inyectadas al agente cuando el backend es `llama-agents`. |
| [agents_cpp.md](./agents_cpp.md) | Reglas del sistema inyectadas al agente cuando el backend es `llamacpp`. |
| [README.md](./README.md) | Documentación oficial del proyecto (descripción, arquitectura, endpoints, guía de instalación). |
| [CAMBIOS.md](./CAMBIOS.md) | Historial de cambios y decisiones técnicas del proyecto. |
| [RULES.md](./RULES.md) | Reglas de desarrollo que el equipo/agente debe respetar (líneas, capas, retrocompatibilidad). |
| [INDICE.md](./INDICE.md) | Este archivo. Mapa de todos los archivos del proyecto. |

---

## 🔵 `routes/` — Capa de presentación (endpoints HTTP)

| Archivo | Endpoint | Función |
|---------|----------|---------|
| [routes/chat.py](./routes/chat.py) | `POST /chat/<session_id>` | Endpoint principal. Recibe el mensaje, orquesta el flujo completo y devuelve la respuesta en streaming SSE. |
| [routes/session.py](./routes/session.py) | `POST /session` | Crea una nueva sesión en el backend `llama-agents`. |
| [routes/permission.py](./routes/permission.py) | `POST /permission` | Aprueba o deniega un permiso de herramienta del agente. |

---

## 🟡 `services/` — Capa de lógica de negocio

| Archivo | Función |
|---------|---------|
| [services/rules.py](./services/rules.py) | Construye el prompt final. Detecta términos biológicos y materia para activar el RAG. En modo tutor inyecta contexto RAG entre las preguntas fallidas y la conversación reciente. |
| [services/rag_service.py](./services/rag_service.py) | Conecta con ChromaDB (`rag/chroma_db/`) para hacer búsqueda semántica por embeddings. Expone `search()` y `get_context_for_prompt()` para inyectar contexto en los prompts. |
| [services/chat_orchestrator.py](./services/chat_orchestrator.py) | Decide a qué backend enviar la petición (`llamacpp` o `llama-agents`). Detecta keywords de quiz para aplicar gramática GBNF. |
| [services/stream_handler.py](./services/stream_handler.py) | Genera el stream SSE normalizado para el cliente. Al terminar, dispara el guardado y la automatización si es un quiz. |
| [services/llamacpp_service.py](./services/llamacpp_service.py) | Cliente HTTP para el endpoint `/completion` (o `/v1/chat/completions`) de llama.cpp. |
| [services/llama_agent.py](./services/llama_agent.py) | Cliente HTTP para la API de `llama-agents` (sesión y chat). |
| [services/grammar_service.py](./services/grammar_service.py) | Carga el archivo `json_quiz.gbnf` e inyecta la gramática en las opciones del request. |
| [services/persistence_service.py](./services/persistence_service.py) | Guarda la respuesta JSON del LLM en disco (`/quizzes/`). También mantiene el historial de sesión en memoria. |
| [services/automation_service.py](./services/automation_service.py) | Ejecuta el comando externo de subida en un proceso background al terminar de generar un quiz. Lo termina al cerrar el proxy con `atexit`. |
| [services/permissions.py](./services/permissions.py) | Lógica de auto-aprobación de herramientas del agente (`write`, `bash`). Envía la respuesta de permiso a `llama-agents`. |

---

## 🔴 `utils/` — Utilidades transversales

| Archivo | Función |
|---------|---------|
| [utils/logger.py](./utils/logger.py) | Configura Loguru. Crea un handler de log por sesión (archivo propio en `/logs/`) con rotación de 5 MB y retención de 7 días. |

---

## 🟣 `rag/` — Indexación y base vectorial

| Archivo/Carpeta | Función |
|---------|---------|
| [rag/index_rag.py](./rag/index_rag.py) | Script offline para indexar los archivos `.md` del RAG en ChromaDB usando embeddings `all-MiniLM-L6-v2`. Se ejecuta manualmente para regenerar el índice. |
| `rag/chroma_db/` | Base vectorial persistente generada por `index_rag.py`. Contiene los embeddings de todo el contenido educativo. **No se sube al repo.** |

### 📄 Contenido educativo (`rag/*.md`)

> Archivos con información de materias de colegio (10mo EGB). El nombre de cada archivo describe su contenido.

| Archivo | Contenido |
|---------|-----------|
| [rag/00_curriculo_gobierno_10mo_EGB.md](./rag/00_curriculo_gobierno_10mo_EGB.md) | Currículo oficial del gobierno para 10mo de EGB |
| [rag/01_libro_enriquecido.md](./rag/01_libro_enriquecido.md) | Libro enriquecido (Unidad 1) |
| [rag/01_unidad_1_clasificacion_seres_vivos.md](./rag/01_unidad_1_clasificacion_seres_vivos.md) | Unidad 1 — Clasificación de los seres vivos |
| [rag/02_unidad_2_reproduccion_celular.md](./rag/02_unidad_2_reproduccion_celular.md) | Unidad 2 — Reproducción celular |
| [rag/tema1_preguntas_sin_responder.md](./rag/tema1_preguntas_sin_responder.md) | Tema 1 — Preguntas sin responder |

---

## 📂 Carpetas de salida (generadas en runtime)

| Carpeta | Contenido |
|---------|-----------|
| `quizzes/` | Archivos JSON de quizzes generados por el LLM. Formato: `data_{tema}_{timestamp}.json`. |
| `logs/` | Logs por sesión (`session_{id}_{timestamp}.log`) y logs de la automatización (`uploader.log`). |
