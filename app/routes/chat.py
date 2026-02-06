import threading
import uuid
from pathlib import Path
from app.routes.agents import Orchestrator
from app.routes.say import speak

from flask import (
    Blueprint,
    current_app,
    make_response as flask_make_response,
    render_template,
    request,
    send_from_directory,
    session,
)
from flask_htmx import make_response
from werkzeug.utils import secure_filename

from app.config import allowed_file

bp = Blueprint("chat", __name__)

agent_orchestrator = Orchestrator()

# Max turns (user+assistant pairs) to keep in session
MAX_HISTORY_TURNS = 20

def _save_upload(file) -> str | None:
    """Save uploaded image; return stored filename (for URL) or None."""
    if not file or file.filename == "":
        return None
    if not allowed_file(file.filename):
        return None
    name = secure_filename(file.filename)
    stem = uuid.uuid4().hex[:12]
    ext = Path(name).suffix.lower()
    stored = f"{stem}{ext}"
    folder = Path(current_app.config["UPLOAD_FOLDER"])
    path = folder / stored
    file.save(path)
    return stored


def _get_history() -> list[tuple[str, str]]:
    """Get conversation history from session as [(role, content), ...] for LangChain."""
    raw = session.get("chat_history", [])
    return [(h["role"], h["content"]) for h in raw]


def _append_to_history(user_msg: str, assistant_msg: str) -> None:
    """Append a turn to session history and trim if needed."""
    history = session.get("chat_history", [])
    history.extend([
        {"role": "human", "content": user_msg},
        {"role": "ai", "content": assistant_msg},
    ])
    session["chat_history"] = history[-(MAX_HISTORY_TURNS * 2) :]


def _process_message(text: str | None, image_filename: str | None) -> str:
    """Process user input with conversational context."""
    if text and text.strip():
        history = _get_history()
        result = agent_orchestrator.ask(text.strip(), history=history)
        response = result.content
        _append_to_history(text.strip(), response)
        return response
    if image_filename:
        return "Not sure what to do with an image."
    return "Send a message or an image to get a reply."


@bp.route("/uploads/<path:filename>")
def uploads(filename: str):
    """Serve uploaded images."""
    folder = current_app.config["UPLOAD_FOLDER"]
    return send_from_directory(str(folder), filename)


@bp.route("/")
def index():
    return render_template(
        "index.html",
        chatbot_name=current_app.config["CHATBOT_NAME"],
    )


@bp.route("/message", methods=["POST"])
def message():
    text = request.form.get("message", "").strip() or None
    image = request.files.get("image")
    image_filename = _save_upload(image) if image else None

    if not text and not image_filename:
        if request.headers.get("HX-Request"):
            r = flask_make_response(
                render_template(
                    "partials/error.html",
                    error="Please enter a message or attach an image.",
                ),
                400,
            )
            r.headers["HX-Retarget"] = "#form-errors"
            r.headers["HX-Reswap"] = "innerHTML"
            return r
        return "Bad Request", 400

    reply = _process_message(text, image_filename)

    if reply and (text or image_filename) and request.form.get("speak"):
        threading.Thread(target=speak, args=(reply,), daemon=True).start()

    if request.headers.get("HX-Request"):
        resp = make_response(
            render_template(
                "partials/bot_message.html",
                bot_message=reply,
                chatbot_name=current_app.config["CHATBOT_NAME"],
            )
        )
        resp.headers["HX-Retarget"] = "#msg-loading"
        resp.headers["HX-Reswap"] = "outerHTML"
        resp.headers["HX-Trigger-After-Swap"] = "focus-input"
        return resp

    return "OK", 200
