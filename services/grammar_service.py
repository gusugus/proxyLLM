from loguru import logger

def apply_quiz_grammar(options):
    """
    Loads and applies the GBNF grammar for JSON quiz generation.
    """
    try:
        # Load from file to allow live edits as requested
        with open("json_quiz.gbnf", "r", encoding="utf-8") as f:
            options["grammar"] = f.read()
        logger.info("[GRAMMAR] JSON Quiz grammar applied")
    except Exception as e:
        logger.error(f"[GRAMMAR] Error loading grammar: {e}")
