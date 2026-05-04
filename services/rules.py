from services.rag_service import get_context_for_prompt

def load_rules(backend="llama-agents"):
    filename = "agents_cpp.md" if backend == "llamacpp" else "agents.md"
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return ""

def apply_rules(user_message: str, backend="llama-agents", preguntas=None,
                materia=None, history=None) -> str:
    """Applies rules. If 'preguntas' or 'materia' present, acts as tutor."""

    # ----- INICIO: NUEVA LÓGICA DE RAG -----
    # Palabras clave biológicas para activar el RAG
    bio_keywords = ['célula', 'reproducción', 'taxonomía', 'clasificación', 'reino', 'dominio',
                    'especie', 'hongo', 'bacteria', 'protista', 'animal', 'planta', 'mitosis',
                    'meiosis', 'evolución', 'biodiversidad', 'ecosistema', 'cadena alimenticia']

    contexto_rag = ""
    # Se activa si es una materia biológica o si el mensaje contiene palabras clave
    if (materia and "natural" in materia.lower()) or any(kw in user_message.lower() for kw in bio_keywords):
        contexto_rag = get_context_for_prompt(user_message)
    # ----- FIN: NUEVA LÓGICA DE RAG -----

    if preguntas or materia or history:
        # Pasamos el contexto_rag a la función de formato del tutor
        return _format_tutor_rules(user_message, preguntas, materia, history, contexto_rag)

    rules = load_rules(backend)
    if not rules:
        return user_message
    # Si no es modo tutor, se mantiene la estructura original, inyectando el contexto al inicio
    return contexto_rag + f"{rules}\n\nUsuario:\n{user_message}"

def _format_tutor_rules(message, preguntas, materia, history, contexto_rag=""):
    """Tutor prompt - formato directo, nada de JSON."""
    # ... (sección de errores_texto sin cambios) ...
    errores_texto = "No hay errores previos."
    if preguntas:
        errores_texto = ""
        for q in preguntas:
            q_text = q.get('question', '...')
            ans = q.get('studentAnswer') or 'No respondió'
            correct = q.get('correctAnswer') or '...'
            errores_texto += f"- {q_text}\n Respuesta del Alumno: {ans} (Respuesta Correcta: {correct})\n"

    # ... (sección de history_texto sin cambios) ...
    history_texto = ""
    if history:
        ultimos = history[-4:]
        history_texto = "Esto es lo que hemos hablado:\n"
        for msg in ultimos:
            if msg["role"] == "user":
                history_texto += f"Preguntaste: {msg['content']}\n"
            else:
                history_texto += f"Te respondí: {msg['content']}\n"

    # ----- AQUÍ ES DONDE SE INYECTA EL CONTEXTO -----
    # Crea el prompt final con el contexto RAG justo después de las preguntas fallidas
    prompt = f"""Eres un profesor de {materia}. Solo hablas de {materia}.

=== PREGUNTAS QUE RESPONDISTE MAL ===
{errores_texto}
=== FIN DE LAS PREGUNTAS MALAS ===

{contexto_rag}

=== CONVERSACIÓN RECIENTE ===
{history_texto}
=== FIN DE LA CONVERSACIÓN ===

REGLAS:
- NO escribas "Profesor:" ni "Alumno:" en tu respuesta.
- NO inventes preguntas.
- Responde DIRECTAMENTE al alumno, como si estuvieras hablando con él.
- Si la pregunta no es de {materia}, di: "Solo puedo ayudarte con {materia}."

El alumno te pregunta: "{message}"

Ahora RESPONDE DIRECTAMENTE (sin etiquetas, sin descripciones):"""
    return prompt