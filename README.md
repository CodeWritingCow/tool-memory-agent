# Tool Memory Agent

A local AI agent built with **Python**, **LangChain**, **LangGraph**, **Ollama**, and **Qwen**. The agent demonstrates **tool calling** and **short-term conversational memory** using LangGraph's in-memory checkpointing.

This project is based on the freeCodeCamp tutorial [How to Build Your Own Local AI Agent with Tool Calling and Memory](https://www.freecodecamp.org/news/how-to-build-your-own-local-ai-agent-with-tool-calling-and-memory/).

## Features

* Runs locally using Ollama and Qwen
* Uses LangChain for agent and tool integration
* Uses LangGraph for agent execution and short-term memory
* Supports tool calling
* Includes a tool for retrieving the current date and time
* Includes a tool for counting words
* Maintains conversation history during the current session

## Tech Stack

* Python
* LangChain
* LangGraph
* Ollama
* Qwen

## Prerequisites

* Python 3.12+
* [Ollama](https://ollama.com/)
* Qwen model compatible with tool calling
* One of the following Python environment managers:

  * [Conda](https://docs.conda.io/)
  * Python `venv`
  * [uv](https://docs.astral.sh/uv/)

## Installation

### 1. Clone the Repository

Clone the repository and navigate into the project directory:

# HTTPS
```bash
git clone https://github.com/CodeWritingCow/tool-memory-agent.git
cd tool-memory-agent
```

# SSH
```bash
git clone git@github.com:CodeWritingCow/tool-memory-agent.git
cd tool-memory-agent
```
### 2. Set Up the Python Environment

Choose **one** of the following methods.

#### Option 1: Conda

Create a Conda environment:

```bash
conda create -n tool-memory-agent python=3.12
```

Activate the environment:

```bash
conda activate tool-memory-agent
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

#### Option 2: Python `venv`

##### macOS / Linux

Create a virtual environment:

```bash
python3 -m venv venv
```

Activate the environment:

```bash
source venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

##### Windows

Create a virtual environment:

```powershell
python -m venv venv
```

Activate the environment in PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Or activate it from Command Prompt:

```cmd
venv\Scripts\activate
```

Install the dependencies:

```powershell
pip install -r requirements.txt
```

#### Option 3: uv

Create a virtual environment:

```bash
uv venv
```

Activate the environment if desired.

##### macOS / Linux

```bash
source .venv/bin/activate
```

##### Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

##### Windows Command Prompt

```cmd
.venv\Scripts\activate
```

Install the dependencies:

```bash
uv pip install -r requirements.txt
```

Alternatively, you can run the agent directly through the uv environment without manually activating it:

```bash
uv run python agent.py
```

## Ollama Setup

Make sure Ollama is installed and running.

Pull the Qwen model used by the agent:

```bash
ollama pull qwen3.5:4b
```

Verify that the model is available:

```bash
ollama list
```

The model name in `agent.py` should match the model installed in Ollama:

```python
CHAT_MODEL = "qwen3.5:4b"
```

## Usage

After activating your environment, run:

```bash
python agent.py
```

With uv, you can also run:

```bash
uv run python agent.py
```

You should see:

```text
Ready! Ask the agent something. It remembers the conversation.

You:
```

The agent provides an interactive prompt. Enter a question and press **Enter**.

### Tool Calling

The agent has access to two tools:

* `get_current_time` — Returns the current local date and time.
* `count_words` — Counts the number of words in supplied text.

For example:

```text
You: What time is it?
```

The agent should call the `get_current_time` tool and return the result.

You can also ask:

```text
You: How many words are in "The quick brown fox jumps over the lazy dog"?
```

The agent can use the `count_words` tool to answer.

Tool calls are displayed in the terminal:

```text
[tool call] get_current_time({})
```

### Short-Term Memory

The agent uses LangGraph's `InMemorySaver` to maintain conversation history.

For example:

```text
You: My favorite programming language is Python.
```

Then ask:

```text
You: What is my favorite programming language?
```

The agent can use the previous conversation to answer.

The conversation is associated with a LangGraph thread:

```python
config = {"configurable": {"thread_id": "thread"}}
```

Because `InMemorySaver` stores the state in memory, the conversation history is lost when the Python process exits.

### Exit the Agent

Enter either:

```text
exit
```

or:

```text
quit
```

to end the interactive session.

## Project Structure

```text
tool-memory-agent/
├── agent.py
├── requirements.txt
└── README.md
```

## How It Works

The agent is created with LangChain's `create_agent()` and a local `ChatOllama` model:

```python
model = ChatOllama(
    model=CHAT_MODEL,
    temperature=0
)
```

The agent is given the available tools and a system prompt:

```python
return create_agent(
    model=model,
    tools=TOOLS,
    system_prompt=SYSTEM_PROMPT,
    checkpointer=checkpointer
)
```

`InMemorySaver` provides short-term memory by saving the conversation state associated with the configured thread ID.

The interactive loop then sends each user message to the agent:

```python
result = agent.invoke(
    {"messages": [{"role": "user", "content": question}]},
    config=config
)
```

## Important

Make sure `agent.py` calls `main()` when executed directly. The bottom of the file should contain:

```python
if __name__ == "__main__":
    main()
```

Without this, running:

```bash
python agent.py
```

will define the functions but never start the interactive prompt.

## License

This project is licensed under the MIT License.
