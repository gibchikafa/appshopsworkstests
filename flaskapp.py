import os

from flask import Blueprint, Flask, jsonify


APP_BASE_URL_PATH = os.getenv("APP_BASE_URL_PATH", "").rstrip("/")

app = Flask(__name__)
bp = Blueprint("app", __name__, url_prefix=APP_BASE_URL_PATH or None)


@bp.get("/health")
def health():
    return jsonify(status="ok")


@bp.get("/")
def home():
    base = APP_BASE_URL_PATH or "/"
    return f"""
    <!doctype html>
    <html>
      <head>
        <meta charset="utf-8" />
        <title>Flask on Hopsworks</title>
      </head>
      <body>
        <h1>Flask on Hopsworks</h1>
        <p>Base path: <code>{base}</code></p>
      </body>
    </html>
    """


app.register_blueprint(bp)
