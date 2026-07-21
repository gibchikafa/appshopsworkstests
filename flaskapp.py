from flask import Blueprint, Flask, jsonify


app = Flask(__name__)
bp = Blueprint("app", __name__, url_prefix="/")


@bp.get("/health")
def health():
    return jsonify(status="ok")


@bp.get("/")
def home():
    return """
    <!doctype html>
    <html>
      <head>
        <meta charset="utf-8" />
        <title>Flask on Hopsworks</title>
      </head>
      <body>
        <h1>Flask on Hopsworks</h1>
        <p>Route prefix: <code>/</code></p>
      </body>
    </html>
    """


app.register_blueprint(bp)
