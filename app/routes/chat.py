import threading
import uuid
from pathlib import Path
from app.utilities.say import speak
from flask import Blueprint, current_app, make_response as flask_make_response, \
        render_template, request, send_from_directory
from flask_htmx import make_response
from werkzeug.utils import secure_filename
from app.config import allowed_file
import requests
# import markdown
import strip_markdown

bp = Blueprint("chat", __name__)


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


def _process_message(text: str | None, image_filename: str | None) -> str:
    """Process user input with conversational context."""
    if text and text.strip():
        payload = {
            "query": text,
            "query-path": None,
            "response" : None,
            "response-path": None,  
        }
        answer = requests.post(f'{current_app.config["AGENT_URL"]}/agent', json=payload)
        
        if answer.status_code == 200:
            # models return markdown, convert to html for display
            return strip_markdown.strip_markdown(answer.text)
        else:
            return "An error occurred while processing your message."
        
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
        threading.Thread(target=speak, args=(reply.content,), daemon=True).start()

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
