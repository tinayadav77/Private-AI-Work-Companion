def detect_intent(text: str) -> str:
    """
    Determine the basic intent of a user's spoken input.
    """

    text = text.lower().strip()

    search_phrases = [
        "find my",
        "find the",
        "find a",
        "find",
        "search for",
        "look for",
        "locate",
        "where is my file",
        "where are my notes",
        "find the pdf",
        "search my files",
        "Help me find the pdf",
        "could you search for",
        "can you help me find",
    ]

    task_phrases = [
        "remind me",
        "i need to",
        "i have to",
        "i should",
        "i must",
        "tomorrow i",
        "today i",
        "later i",
        "don't forget",
        "do not forget",
        "finish",
        "complete",
        "submit",
        "prepare",
        "revise",
        "study",
    ]

    question_phrases = [
        "what is",
        "what are",
        "why is",
        "why are",
        "how do",
        "how does",
        "how can",
        "where is",
        "can you explain",
        "?",
    ]

    if any(phrase in text for phrase in search_phrases):
        return "search"

    if any(phrase in text for phrase in task_phrases):
        return "task"

    if any(phrase in text for phrase in question_phrases):
        return "question"

    return "conversation"