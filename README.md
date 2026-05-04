# 🎓 EduProxy — Proxy Inteligente para Tutoría Educativa con LLM

**EduProxy** es un servidor proxy (API REST) construido en Flask que actúa como intermediario entre un frontend educativo y modelos de lenguaje (LLM) locales. Su propósito principal es potenciar una plataforma de aprendizaje gamificada tipo *Kahoot* con inteligencia artificial, permitiendo:

- **Generación automática de quizzes** en formato JSON a partir de contenido educativo.
- **Tutoría personalizada** basada en las preguntas que el alumno respondió mal.
- **Streaming en tiempo real** (SSE) de las respuestas del LLM al cliente.

---

## 📋 Tabla de Contenidos

- [Objetivos del Proyecto](#-objetivos-del-proyecto)
- [Arquitectura General](#-arquitectura-general)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Requerimientos](#-requerimientos)
- [Instalación y Configuración](#-instalación-y-configuración)
- [Variables de Entorno](#-variables-de-entorno)
- [Endpoints de la API](#-endpoints-de-la-api)
- [Flujos Principales](#-flujos-principales)
- [Base de Datos](#-base-de-datos)
- [Contenido RAG](#-contenido-rag)
- [Reglas de Desarrollo](#-reglas-de-desarrollo)

---

## 🎯 Objetivos del Proyecto

1. **Generar quizzes educativos automáticamente**: El profesor solicita X preguntas sobre un tema y el LLM genera un JSON estructurado listo para inyectarse en la plataforma de juego (Rahoot).
2. **Modo Tutor personalizado**: Cuando un alumno falla preguntas en un quiz, el sistema activa un tutor IA que explica los errores, usando el historial de conversación para mantener contexto.
3. **Ser agnóstico al backend de LLM**: Soporta dos backends intercambiables:
   - **llama.cpp** (servidor local de inferencia, por defecto)
   - **llama-agents** (orquestador multi-agente)
4. **Automatización end-to-end**: Al generar un quiz, automáticamente guarda el JSON y ejecuta un comando para subirlo a la plataforma de juego.
5. **Logging detallado**: Cada sesión genera su propio archivo de log con el prompt completo, pensamiento del LLM, y la respuesta generada token por token.

---

## 🏗 Arquitectura General

```
┌──────────────┐       ┌──────────────────┐       ┌─────────────────┐
│   Frontend   │──────▶│   EduProxy       │──────▶│   LLM Backend   │
│  (Rahoot)    │  HTTP │   (Flask :5000)   │  HTTP │  llama.cpp :8080│
│              │◀──SSE─│                  │◀──SSE─│  ó llama-agents │
└──────────────┘       └──────────────────┘       └─────────────────┘
                              │
                              ├── Inyección de reglas/prompts
                              ├── Gramática GBNF para JSON
                              ├── Guardado de quizzes a disco
                              └── Ejecución de automatización
```

**Patrón de diseño**: Arquitectura por capas (tipo MVC) con separación estricta:
- **`routes/`** — Capa de presentación (endpoints HTTP)
- **`services/`** — Capa de lógica de negocio
- **`utils/`** — Utilidades transversales

---

## 📂 Estructura del Proyecto

```
proxy/
├── app.py                      # Punto de entrada de Flask
├── config.py                   # Carga de variables de entorno
├── requirements.txt            # Dependencias de Python
├── .env                        # Variables de entorno locales
│
├── routes/                     # Capa de rutas (Blueprints)
│   ├── chat.py                 # POST /chat/<session_id> — Endpoint principal
│   ├── session.py              # POST /session — Crear sesión de agente
│   └── permission.py           # POST /permission — Permisos de herramientas
│
├── services/                   # Capa de lógica de negocio
│   ├── rules.py                # Inyección de prompts y modo tutor
│   ├── chat_orchestrator.py    # Selección y ruteo al backend LLM
│   ├── stream_handler.py       # Generador SSE y post-procesamiento
│   ├── llamacpp_service.py     # Cliente HTTP para llama.cpp
│   ├── llama_agent.py          # Cliente HTTP para llama-agents
│   ├── grammar_service.py      # Carga de gramática GBNF
│   ├── persistence_service.py  # Guardado de JSON en disco + historial
│   ├── automation_service.py   # Ejecución de procesos background
│   └── permissions.py          # Lógica de auto-aprobación de herramientas
│
├── utils/
│   └── logger.py               # Configuración de Loguru (por sesión)
│
├── rag/                        # Contenido educativo (RAG)
│   ├── 00_curriculo_gobierno_10mo_EGB.md
│   ├── 01_libro_enriquecido.md
│   ├── 01_unidad_1_clasificacion_seres_vivos.md
│   ├── 02_unidad_2_reproduccion_celular.md
│   ├── libroBachillerato.md
│   └── imagenes/               # Recursos gráficos del contenido
│
├── quizzes/                    # Quizzes generados (salida JSON)
├── logs/                       # Logs por sesión y de automatización
│
├── agents.md                   # Reglas del agente (modo llama-agents)
├── agents_cpp.md               # Reglas del agente (modo llama.cpp)
├── json_quiz.gbnf              # Gramática GBNF para formato de quiz
│
├── CAMBIOS.md                  # Historial de cambios del proyecto
└── RULES.md                    # Reglas de desarrollo para contribuidores
```

---

## ⚙ Requerimientos

### Software necesario

| Software        | Versión mínima | Propósito                                      |
|-----------------|----------------|-------------------------------------------------|
| **Python**      | 3.10+          | Runtime del proxy                               |
| **pip**         | 21+            | Gestor de paquetes Python                       |
| **llama.cpp**   | Reciente       | Servidor de inferencia LLM local (backend principal) |
| **Node.js/pnpm**| 18+            | Para la automatización de subida de quizzes (opcional) |

### Dependencias de Python

Definidas en `requirements.txt`:

| Paquete            | Versión  | Descripción                                                   |
|--------------------|----------|---------------------------------------------------------------|
| `flask`            | 3.0.2    | Framework web para la API REST                                |
| `flask-cors`       | 4.0.0    | Soporte CORS para peticiones del frontend                     |
| `requests`         | 2.31.0   | Cliente HTTP para comunicarse con los backends LLM            |
| `python-dotenv`    | 1.0.1    | Carga de variables desde `.env`                               |
| `gunicorn`         | 21.2.0   | Servidor WSGI para producción (multi-worker)                  |
| `loguru`           | 0.7.2    | Logging avanzado con rotación, colores y filtros por sesión   |

### Modelo LLM

Se requiere un modelo compatible con llama.cpp ejecutándose localmente. El proyecto está diseñado y probado con modelos que soportan **thinking** (razonamiento interno), como Qwen3 o similares.

---

## 🚀 Instalación y Configuración

### 1. Clonar el repositorio

```bash
git clone <url-del-repo>
cd proxy
```

### 2. Crear entorno virtual e instalar dependencias

```bash
python -m venv venv
source venv/bin/activate        # Linux/Mac
# venv\Scripts\activate         # Windows

pip install -r requirements.txt
```

### 3. Configurar variables de entorno

Copiar y editar el archivo `.env`:

```bash
cp .env.example .env
# Editar .env con tus rutas y configuración
```

### 4. Iniciar el servidor de llama.cpp

```bash
# Ejemplo con un modelo Qwen3
./llama-server -m modelo.gguf -c 4096 --port 8080
```

### 5. Ejecutar el proxy

```bash
# Desarrollo
python app.py

# Producción
gunicorn app:app --bind 0.0.0.0:5000 --workers 4
```

El proxy estará disponible en `http://localhost:5000`.

---

## 🔐 Variables de Entorno

| Variable                | Default                    | Descripción                                              |
|-------------------------|----------------------------|----------------------------------------------------------|
| `LLAMA_AGENT_URL`       | —                          | URL del servidor llama-agents                            |
| `LLAMACPP_URL`          | `http://localhost:8080`    | URL del servidor llama.cpp                               |
| `AUTO_APPROVE`          | `true`                     | Auto-aprobar permisos de herramientas del agente         |
| `QUIZ_SAVE_DIR`         | `./quizzes`                | Directorio donde se guardan los quizzes generados        |
| `QUIZ_UPLOAD_COMMAND`   | `npm start`                | Comando para subir quiz a la plataforma de juego         |
| `QUIZ_UPLOAD_LOG`       | `./logs/uploader.log`      | Archivo de log del proceso de subida                     |
| `USE_CHAT_COMPLETIONS`  | `false`                    | Usar endpoint `/v1/chat/completions` en vez de `/completion` |

---

## 📡 Endpoints de la API

### `POST /chat/<session_id>`

Endpoint principal. Envía un mensaje al LLM y devuelve la respuesta como stream SSE.

**Request Body:**

```json
{
  "message": "Crea 5 preguntas sobre la célula",
  "backend": "llamacpp",
  "temperature": 0.7,
  "max_tokens": 2048,
  "thinking": true,
  "materia": "Ciencias Naturales",
  "preguntas": [],
  "history": []
}
```

| Campo        | Tipo     | Descripción                                                      |
|--------------|----------|------------------------------------------------------------------|
| `message`    | string   | Mensaje del usuario                                              |
| `backend`    | string   | `"llamacpp"` o `"llama-agents"` (default: `"llamacpp"`)          |
| `temperature`| float    | Temperatura de generación (0-2)                                  |
| `max_tokens` | int      | Máximo de tokens a generar                                       |
| `thinking`   | bool     | Habilitar pensamiento interno del LLM (default: `true`)         |
| `materia`    | string   | Materia del contexto educativo (activa modo tutor)               |
| `preguntas`  | array    | Preguntas fallidas del alumno (activa modo tutor)                |
| `history`    | array    | Historial de conversación `[{role, content}]` (del cliente)      |

**Response:** Stream SSE con eventos:

- `text_delta` — Chunk de texto generado `{content, thought}`
- `completed` — Fin de generación `{reason, stats}`

---

### `POST /session`

Crea una nueva sesión en llama-agents.

**Response:**
```json
{
  "session_id": "uuid-de-la-sesion"
}
```

---

### `POST /permission`

Aprueba o deniega un permiso de herramienta del agente.

**Request Body:**
```json
{
  "request_id": "id-del-permiso",
  "allow": true
}
```

---

## 🔄 Flujos Principales

### Flujo 1: Generación de Quiz

```
1. Frontend envía: POST /chat/new { message: "5 preguntas sobre la célula" }
2. rules.py → Inyecta reglas del agente (agents_cpp.md)
3. chat_orchestrator.py → Detecta keywords "pregunta" → aplica gramática GBNF
4. llamacpp_service.py → Envía prompt + gramática a llama.cpp
5. stream_handler.py → Recibe SSE, acumula respuesta
6. Al terminar (stop=true):
   a. persistence_service.py → Guarda JSON en /quizzes/
   b. automation_service.py → Ejecuta comando de subida
7. Cliente recibe el quiz completo vía SSE
```

### Flujo 2: Modo Tutor

```
1. Frontend envía: POST /chat/session123 {
     message: "No entendí lo de la mitosis",
     materia: "Ciencias Naturales",
     preguntas: [{ question: "...", studentAnswer: "...", correctAnswer: "..." }],
     history: [...]
   }
2. rules.py → Construye prompt de tutor con errores + historial
3. LLM responde como profesor, explicando los errores
4. Cliente recibe respuesta en streaming
```

---

## 🗄 Base de Datos

> **Este proyecto NO utiliza base de datos.**

Todo el estado se maneja de la siguiente manera:

| Dato                    | Almacenamiento                                     |
|-------------------------|----------------------------------------------------|
| Quizzes generados       | Archivos JSON en disco (`/quizzes/`)               |
| Historial de sesión     | Manejado por el **cliente** (frontend)             |
| Logs de interacción     | Archivos `.log` en disco (`/logs/`)                |
| Sesiones de agente      | Manejadas por el backend llama-agents              |
| Configuración           | Variables de entorno (`.env`)                      |

No hay persistencia en base de datos relacional ni NoSQL. Los quizzes se generan como archivos JSON independientes con la convención de nombres:

```
data_{tema}_{timestamp_unix}.json
```

---

## 📚 Contenido RAG

El directorio `rag/` contiene el material educativo de referencia, alineado con el **Currículo Oficial de Ecuador para 10mo año de EGB** en la materia de **Ciencias Naturales**. Este contenido sirve como base de conocimiento para la generación de quizzes y las respuestas del tutor.

### Archivos disponibles:

| Archivo                                          | Contenido                                         |
|--------------------------------------------------|----------------------------------------------------|
| `00_curriculo_gobierno_10mo_EGB.md`              | Currículo oficial: temas, objetivos, criterios de evaluación |
| `01_libro_enriquecido.md`                        | Resumen enriquecido del libro de texto             |
| `01_unidad_1_clasificacion_seres_vivos.md`       | Unidad 1: Clasificación y taxonomía                |
| `02_unidad_2_reproduccion_celular.md`            | Unidad 2: Reproducción celular                     |
| `libroBachillerato.md`                           | Referencia de libro de bachillerato                |

---

## 📏 Reglas de Desarrollo

El proyecto sigue reglas estrictas documentadas en `RULES.md`:

1. **Archivos ≤ 60 líneas** — Para facilitar la lectura por parte de otros LLMs. Si un archivo supera este límite, se divide en archivos más pequeños.
2. **Arquitectura por capas** — Separación clara entre rutas, servicios y utilidades.
3. **Responsabilidad única** — Cada archivo/función hace una sola cosa.
4. **Reutilización** — Servicios genéricos (`persistence_service`, `automation_service`) en vez de servicios acoplados a un dominio.
5. **Retrocompatibilidad** — Los cambios deben ser compatibles con versiones anteriores.
6. **Prompts protegidos** — No modificar la estructura de prompts en `rules.py` sin petición explícita del usuario.
7. **Documentación** — Mantener `CAMBIOS.md` actualizado con cada modificación.

---

## 📝 Licencia

*Por definir.*

---

> **Última actualización:** Mayo 2026
