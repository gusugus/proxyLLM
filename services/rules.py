def load_rules(backend="llama-agents"):
    filename = "agents_cpp.md" if backend == "llamacpp" else "agents.md"
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return ""

def apply_rules(user_message: str, backend="llama-agents", preguntas=None, materia=None, history=None) -> str:
    """Applies rules. If 'preguntas' or 'materia' present, acts as tutor."""
    if preguntas or materia or history:
        return _format_tutor_rules(user_message, preguntas, materia, history)
    rules = load_rules(backend)
    if not rules: return user_message
    return f"{rules}\n\nUsuario:\n{user_message}"

def _format_tutor_rules(message, preguntas, materia, history):
    """Tutor prompt - formato directo, nada de JSON."""
    
    # Construir errores
    errores_texto = "No hay errores previos."
    if preguntas:
        errores_texto = ""
        for q in preguntas:
            q_text = q.get('question', '...')
            ans = q.get('studentAnswer') or 'No respondió'
            correct = q.get('correctAnswer') or '...'
            errores_texto += f"- {q_text}\n  Respuesta del Alumno: {ans} (Respuesta Correcta: {correct})\n"
    
    # Construir historial (solo lo último, sin etiquetas de "Alumno:" "Profesor:")
    history_texto = ""
    if history:
        ultimos = history[-4:]
        history_texto = "Esto es lo que hemos hablado:\n"
        for msg in ultimos:
            if msg["role"] == "user":
                history_texto += f"Preguntaste: {msg['content']}\n"
            else:
                history_texto += f"Te respondí: {msg['content']}\n"
    
    prompt = f"""Eres un profesor de {materia}. Solo hablas de {materia}.

=== PREGUNTAS QUE RESPONDISTE MAL ===
{errores_texto}
=== FIN DE LAS PREGUNTAS MALAS ===

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