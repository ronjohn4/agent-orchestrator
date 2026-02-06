# Home Assistant/Office Chatbot

This is my AI learning project.  

[x] Orchestrator Agent
[] Sub-agents
   [] One sub-agent for each tool
   [] sub-agent will use the pattern most effective for this tool call
[] Tools
   [] GetWeather
   [] GetDateTime
   [] web search
[] LLM
   [] minimize the number of different LLMs used
   [] ideally use locally hosted LLMs
[] RAG
   [] Local files
      [] persist vector db
      [] update vector db when source files change
   [] LangChain online documentation
[] User feedback loop
   [] Chat thumbs up/down
[] Monitoring
   [] token usage
   [] costs
[] logging
   [] for debugging
[] memory
   [] previous conversation
      [] determine when the topic has chamged
      [] determine information that is relevant to the job, not the task
      [] age out old information that is no longer relevant
   [] context 
      [] how to decide what is relevant for the current question and the current conversation
[] timing
   [] job - like being the research assistant
   [] project - like building a specific piece of software
   [] task - the specific work being done now
   [] question  - this specific turn
[] changes based on time
   [] when does the graph change, the sub-agents that can be used
   [] how decide what is relevant and to save for the future
   [] how to organize the future knowledge
[] todo queue
   [] list of tasks that aren't important now but can be worked on in spare time
      [] prioritizing this list
   [] how to suspend current work and add tot he todo queue
      [] could happen when a human in the loop question comes up and the human isn't available
[] MCP Server
   [] MyData integration (another side project that exposes a set ot REST APIs)
[] speech
   [x] toggle on/off talking
   [x] allow spoken input
   [] always listen then contribute when appropriate



A minimal chatbot web app built with **Flask** and **HTMX**. The chatbot name is configurable, and it accepts **text** or **image** uploads (or both).

## Features

- **Configurable name** – Set `CHATBOT_NAME` in `.env` or environment.
- **Text input** – Type messages in the chat input.
- **Image upload** – Attach images (PNG, JPEG, GIF, WebP) via the paperclip button.
- **HTMX** – No full-page reloads; new messages are appended via HTMX.

## Project structure

```
agent-orchestrator/
├── app/
│   ├── __init__.py       # App factory, HTMX, config
│   ├── config.py         # CHATBOT_NAME, upload settings
│   ├── routes/
│   │   ├── __init__.py
│   │   └── chat.py       # Chat UI, /message (text + image), /uploads
│   ├── static/
│   │   └── css/
│   │       └── style.css
│   └── templates/
│       ├── base.html
│       ├── index.html    # Chat layout + form
│       └── partials/
│           ├── error.html
│           └── messages.html
├── uploads/              # Stored images (gitignored except .gitkeep)
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
└── run.py
```

## Requirements

- **Python 3.10+**
- Dependencies in `requirements.txt` (Flask, Flask-HTMX, python-dotenv)

## Setup

1. **Clone and enter the project**

   ```bash
   cd agent-orchestrator
   ```

2. **Create a virtualenv and install dependencies**

   ```bash
   python -m venv .venv
   .venv\Scripts\activate   # Windows
   pip install -r requirements.txt
   ```

3. **Configure environment**

   ```bash
   copy .env.example .env
   ```

   Edit `.env` and set at least:

   - `CHATBOT_NAME` – Name shown in the UI (e.g. `My Bot`).
   - `SECRET_KEY` – Use a random string in production.

4. **Run the app**

   ```bash
   python run.py
   ```

   Open http://localhost:5000 (or the `PORT` from `.env`).

## Configuration

| Variable        | Description                         | Default    |
|----------------|-------------------------------------|------------|
| `CHATBOT_NAME` | Name shown in header and responses  | `Assistant`|
| `SECRET_KEY`   | Flask secret key                    | dev default|
| `FLASK_DEBUG`  | `1` for debug mode                  | `0`        |
| `PORT`         | Server port                         | `5000`     |
| `UPLOAD_FOLDER`| Directory for uploaded images       | `uploads`  |

## Wiring an LLM

Message processing is currently a **placeholder** in `app/routes/chat.py`:

```python
def _process_message(text: str | None, image_filename: str | None) -> str:
    """Replace with your LLM / vision API call."""
    ...
```

- Use `text` for the user’s message.
- Use `image_filename` to build the path under `UPLOAD_FOLDER` and pass the image to a vision-capable model (e.g. OpenAI GPT-4V, Claude, etc.).
- Return the assistant’s reply string.

## License

MIT.
