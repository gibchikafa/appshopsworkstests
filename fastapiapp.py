from fastapi import FastAPI
from fastapi.responses import HTMLResponse


app = FastAPI(title="Hopsworks FastAPI App")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <!doctype html>
    <html>
      <head>
        <meta charset="utf-8" />
        <title>FastAPI on Hopsworks</title>
      </head>
      <body>
        <h1>FastAPI on Hopsworks</h1>
        <p>Route prefix: <code>/</code></p>
      </body>
    </html>
    """
