# Flask + HTMX Chatbot

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
