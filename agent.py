from datetime import datetime

from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from langgraph.checkpoint.memory import InMemorySaver

CHAT_MODEL = "qwen3.5:4b" # Ollama chat model. Must support tool calling.

SYSTEM_PROMPT = (
    "You are a helpful assistant with access to tools for getting the current time and counting words in text. "
    "Use tools when the user's request needs one. "
    "If the question doesn't need a tool, answer directly. "
    "If a tool returns an error, explain the error plainly."
)

# ----- Tools -----
@tool
def get_current_time() -> str:
    """Return the current local date and time.
    Use this when the user asks what time or date it is.
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@tool
def count_words(text: str) -> int:
    """Count the number of words in a piece of text.
    Use this when the user asks how long a piece of writing is,
    or asks you to count the words in something they've shared.
    Returns the word count as an integer.
    """
    return len(text.split())


TOOLS = [get_current_time, count_words]

# ----- Agent -----
def build_agent():
    model = ChatOllama(model=CHAT_MODEL, temperature=0)

    # InMemorySaver keeps conversation history in memory, keyed by thread ID.
    # When the process exits, the history is gone because of short-term memory.
    checkpointer = InMemorySaver()

    return create_agent(
        model=model,
        tools=TOOLS,
        system_prompt=SYSTEM_PROMPT,
        memory_saver=checkpointer
    )