# appshopsworkstests

This repository contains small examples that can be deployed as Hopsworks apps from Git:

- `fastapiapp.py`
- `flaskapp.py`
- `gradioapp.py`
- `streamlitapp.py`

The apps are written so they work behind the Hopsworks app proxy. Git-backed apps are cloned on every app start.

## Deploy with `hopsworks-api`

Use the Python SDK to create and start an app from this repository.

```python
import os

import hopsworks


project = hopsworks.login(
    host="10.114.123.124",
    port=443,
    api_key_value=os.environ["HOPSWORKS_API_KEY"],
)
apps = project.get_app_api()


fastapi_app = apps.create_app(
    name="fastapifromgithub",
    app_kind="CUSTOM",
    git_url="https://github.com/gibchikafa/appshopsworkstests.git",
    git_provider="GitHub",
    git_branch="main",
    entrypoint_command=(
        'bash -lc "python -m pip install --no-cache-dir fastapi uvicorn && '
        'exec python -m uvicorn fastapiapp:app --host 0.0.0.0 --port \\"$APP_PORT\\""'
    ),
    app_port=8080,
)
fastapi_app.run()
print(fastapi_app.app_url)
```

```python
import os

import hopsworks


project = hopsworks.login(
    host="10.114.123.124",
    port=443,
    api_key_value=os.environ["HOPSWORKS_API_KEY"],
)
apps = project.get_app_api()


flask_app = apps.create_app(
    name="flaskfromgithub",
    app_kind="CUSTOM",
    git_url="https://github.com/gibchikafa/appshopsworkstests.git",
    git_provider="GitHub",
    git_branch="main",
    entrypoint_command=(
        'bash -lc "python -m pip install --no-cache-dir flask && '
        'exec python -m flask --app flaskapp run --host 0.0.0.0 --port \\"$APP_PORT\\""'
    ),
    app_port=8080,
)
flask_app.run()
print(flask_app.app_url)
```

```python
import os

import hopsworks


project = hopsworks.login(
    host="10.114.123.124",
    port=443,
    api_key_value=os.environ["HOPSWORKS_API_KEY"],
)
apps = project.get_app_api()


streamlit_app = apps.create_app(
    name="streamlitfromgithub",
    app_kind="STREAMLIT",
    git_url="https://github.com/gibchikafa/appshopsworkstests.git",
    git_provider="GitHub",
    git_branch="main",
    entrypoint_script="streamlitapp.py",
)
streamlit_app.run()
print(streamlit_app.app_url)
```

```python
import os

import hopsworks


project = hopsworks.login(
    host="10.114.123.124",
    port=443,
    api_key_value=os.environ["HOPSWORKS_API_KEY"],
)
apps = project.get_app_api()


gradio_app = apps.create_app(
    name="gradiofromgithub",
    app_kind="CUSTOM",
    git_url="https://github.com/gibchikafa/appshopsworkstests.git",
    git_provider="GitHub",
    git_branch="main",
    entrypoint_command=(
        'bash -lc "python -m pip install --no-cache-dir gradio && '
        'exec python gradioapp.py"'
    ),
    app_port=7860,
)
gradio_app.run()
print(gradio_app.app_url)
```

## Notes

- `GitHub`, `GitLab`, and `BitBucket` are supported Git providers.
- For custom apps, the app port is configured by Hopsworks and exposed through `APP_PORT`.
- Gradio apps in this repository run on port `7860`.
- For Streamlit Git apps, the entrypoint script must be a Python file relative to the repository root.
- The repository path is cloned into the app container on every start, so changes in Git are picked up on the next restart/redeploy.

If you already have credentials configured in Hopsworks for your Git provider, the app launcher will use them automatically.

## Deploy with the `hops` CLI

The same apps can be created from the command line:

```bash
hops app create fastapifromgithub \
  --app-kind CUSTOM \
  --git-url https://github.com/gibchikafa/appshopsworkstests.git \
  --git-provider GitHub \
  --git-branch main \
  --entrypoint-command 'bash -lc "python -m pip install --no-cache-dir fastapi uvicorn && exec python -m uvicorn fastapiapp:app --host 0.0.0.0 --port \"$APP_PORT\""' \
  --app-port 8080
```

```bash
hops app create flaskfromgithub \
  --app-kind CUSTOM \
  --git-url https://github.com/gibchikafa/appshopsworkstests.git \
  --git-provider GitHub \
  --git-branch main \
  --entrypoint-command 'bash -lc "python -m pip install --no-cache-dir flask && exec python -m flask --app flaskapp run --host 0.0.0.0 --port \"$APP_PORT\""' \
  --app-port 8080
```

```bash
hops app create gradiofromgithub \
  --app-kind CUSTOM \
  --git-url https://github.com/gibchikafa/appshopsworkstests.git \
  --git-provider GitHub \
  --git-branch main \
  --entrypoint-command 'bash -lc "python -m pip install --no-cache-dir gradio && exec python gradioapp.py"' \
  --app-port 7860
```

```bash
hops app create streamlitfromgithub \
  --app-kind STREAMLIT \
  --git-url https://github.com/gibchikafa/appshopsworkstests.git \
  --git-provider GitHub \
  --git-branch main \
  --entrypoint-script streamlitapp.py
```

Add `--start` if you want the CLI to start the app immediately after creation and wait for it to become serving.
