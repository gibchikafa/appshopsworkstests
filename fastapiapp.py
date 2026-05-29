import os

from fastapi import FastAPI
from fastapi.responses import HTMLResponse


APP_BASE_URL_PATH = os.getenv("APP_BASE_URL_PATH", "").rstrip("/")
app = FastAPI(title="Hopsworks FastAPI App")


@app.get(f"{APP_BASE_URL_PATH}/health")
def health():
    return {"status": "ok"}


@app.get(f"{APP_BASE_URL_PATH}/", response_class=HTMLResponse)
def home():
    base = APP_BASE_URL_PATH or "/"
    return f"""
    <!doctype html>
    <html>
      <head>
        <meta charset="utf-8" />
        <title>FastAPI on Hopsworks</title>
      </head>
      <body>
        <h1>FastAPI on Hopsworks</h1>
        <p>Base path: <code>{base}</code></p>
      </body>
    </html>
    """
