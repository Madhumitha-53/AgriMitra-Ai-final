import os

from langchain_groq import ChatGroq

from ai.prompt import prompt


groq_api_key = os.getenv("GROQ_API_KEY")
groq = ChatGroq(
    api_key=groq_api_key,
    model=os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")
) if groq_api_key else None


def get_response(question):
    if not question or not question.strip():
        return "Please ask a farming question."

    if groq is None:
        return "Groq API key is not configured. Please add GROQ_API_KEY to the environment."

    try:
        response = (prompt | groq).invoke({"question": question})
        return response.content
    except Exception as exc:  # pragma: no cover - handled by the chat UI
        raise RuntimeError(f"AI model request failed: {exc}") from exc