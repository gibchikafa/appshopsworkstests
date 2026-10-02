# appshopsworkstests

This repository contains small examples that can be deployed as Hopsworks apps from Git:

- `expressapp.js`
- `fastapiapp.py`
- `flaskapp.py`
- `gradioapp.py`
- `streamlitapp.py`
- `trinoapp.mjs` — preview offline feature-group rows with the JavaScript Trino client

The apps are written for Hopsworks root routing with app base path `/`. Git-backed apps are cloned on every app start.

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


express_app = apps.create_app(
    name="expressfromgithub",
    app_kind="CUSTOM",
    git_url="https://github.com/gibchikafa/appshopsworkstests.git",
    git_provider="GitHub",
    git_branch="main",
    entrypoint_command=(
        'bash -lc "npm install express && '
        'exec node expressapp.js"'
    ),
    app_port=8080,
    app_base_path="/",
)
express_app.run()
print(express_app.app_url)
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


fastapi_app = apps.create_app(
    name="fastapifromgithub",
    app_kind="CUSTOM",
    git_url="https://github.com/gibchikafa/appshopsworkstests.git",
    git_provider="GitHub",
    git_branch="main",
    entrypoint_command=(
        'bash -lc "python -m uv pip install --no-cache fastapi uvicorn && '
        'exec python -m uvicorn fastapiapp:app --host 0.0.0.0 --port \\"$APP_PORT\\""'
    ),
    app_port=8080,
    app_base_path="/",
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
        'bash -lc "python -m uv pip install --no-cache flask && '
        'exec python -m flask --app flaskapp run --host 0.0.0.0 --port \\"$APP_PORT\\""'
    ),
    app_port=8080,
    app_base_path="/",
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
    app_base_path="/",
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
        'bash -lc "python -m uv pip install --no-cache gradio && '
        'exec python gradioapp.py"'
    ),
    app_port=7860,
    app_base_path="/",
)
gradio_app.run()
print(gradio_app.app_url)
```

## JavaScript: read a feature group with Trino

`trinoapp.mjs` serves a page with a **Load feature group** button and a results
table. It runs the SQL query in Node.js with `trino-client`, follows every result
page, and displays SQL and connection errors. `/api/features` returns the same
data as JSON; `/health` checks app readiness without querying Trino.

For an Iceberg feature group named `customers`, version `1`, in project
`myproject`, the query is equivalent to:

```sql
SELECT * FROM iceberg.myproject.customers_1 LIMIT 100
```

Use the catalog, schema, and versioned table shown in your project's **Query
Engine**. The default schema is the project name lowercased. Set `TRINO_SCHEMA`
if your installation exposes a different schema, or you are reading an accessible
feature group from another project. This reads offline data from a table exposed
through Trino; it does not perform online feature lookups. The default `iceberg`
catalog requires an Iceberg-backed feature group visible in that catalog.

Hopsworks-managed Trino uses HTTPS and project-user credentials. The small
`start_trinoapp.py` launcher uses the installed Hopsworks SDK to discover the
coordinator and retrieve the current project user's Trino credentials. It passes
them to Node.js through the process environment without printing them. All data
queries and the web app are JavaScript.

Create the app from a notebook or other authenticated Hopsworks SDK session:

```python
import hopsworks

project = hopsworks.login()
app = project.get_app_api().create_app(
    name="trinofeaturegroup",
    app_kind="CUSTOM",
    git_url="https://github.com/gibchikafa/appshopsworkstests.git",
    git_provider="GitHub",
    git_branch="main",
    entrypoint_command=(
        'bash -lc "npm install --no-save --package-lock=false trino-client@0.2.9 && '
        'exec python start_trinoapp.py"'
    ),
    app_port=8080,
    app_base_path="/",
    readiness_probe_path="/health",
    env_vars={
        "FEATURE_GROUP_NAME": "customers",  # Replace with your feature group.
        "FEATURE_GROUP_VERSION": "1",
        # "TRINO_SCHEMA": "other_schema",  # Optional override.
    },
)
app.run()
print(app.app_url)
```

The Git branch must contain these example files before starting the app. The app
environment needs Node.js, npm, and a Hopsworks SDK with `project.get_trino_api()`.
Use **Root routing**, app base path `/`, and readiness path `/health` when creating
the app through the UI. The startup command installs the npm dependency, so the
pod needs npm registry access.

Configuration:

| Variable | Default | Purpose |
| --- | --- | --- |
| `FEATURE_GROUP_NAME` | `customers` | Feature group name without the version suffix |
| `FEATURE_GROUP_VERSION` | `1` | Feature group version; queries `<name>_<version>` |
| `TRINO_CATALOG` | `iceberg` | Catalog exposing the offline table |
| `TRINO_SCHEMA` | Lowercased project name via launcher | Schema shown in Query Engine |
| `APP_PORT` | `8080` | Injected by Hopsworks |
| `NODE_EXTRA_CA_CERTS` | `/tmp/ca_chain.pem` when present | PEM CA bundle for the Trino HTTPS certificate |

For a standalone Trino endpoint, or to run Node.js directly without the launcher,
install `trino-client@0.2.9` and set `TRINO_SERVER`, `TRINO_USER`, `TRINO_SCHEMA`,
and the feature-group variables, then run `node trinoapp.mjs`. Also provide
`TRINO_PASSWORD` when Basic authentication is required and `NODE_EXTRA_CA_CERTS`
for a private CA. The launcher always selects Hopsworks' managed endpoint and
credentials; direct Node.js mode uses your supplied settings. A Hopsworks API key
is not the Trino password. The endpoint must expose the feature group's actual
offline table; running a separate Trino server alone does not register it.

The example pins the unscoped `trino-client@0.2.9` package to match the original
`import pkg from "trino-client"` API.

References: [Hopsworks Trino API](https://docs.hopsworks.ai/latest/python-api/hopsworks/core/trino_api/),
[Query Engine](https://docs.hopsworks.ai/latest/user_guides/projects/trino/query_engine/),
[Trino JavaScript client](https://github.com/trinodb/trino-js-client).

## Notes

- `GitHub`, `GitLab`, and `BitBucket` are supported Git providers.
- For custom apps, the app port is configured by Hopsworks and exposed through `APP_PORT`.
- Install Python dependencies with plain `uv pip install` (no `--system`). The app container ships a Python virtualenv that is first on `PATH` and writable by the app user; `--system` bypasses it and targets the read-only OS interpreter, so the install fails with `Permission denied` and, even if it succeeded, `python` would not see the packages.
- Gradio apps in this repository run on port `7860`.
- For Streamlit Git apps, the entrypoint script must be a Python file relative to the repository root.
- The repository path is cloned into the app container on every start, so changes in Git are picked up on the next restart/redeploy.

If you already have credentials configured in Hopsworks for your Git provider, the app launcher will use them automatically.

## Deploy with the `hops` CLI

The same apps can be created from the command line:

```bash
hops app create expressfromgithub \
  --app-kind CUSTOM \
  --git-url https://github.com/gibchikafa/appshopsworkstests.git \
  --git-provider GitHub \
  --git-branch main \
  --entrypoint-command 'bash -lc "npm install express && exec node expressapp.js"' \
  --app-port 8080 \
  --app-base-path /
```

```bash
hops app create fastapifromgithub \
  --app-kind CUSTOM \
  --git-url https://github.com/gibchikafa/appshopsworkstests.git \
  --git-provider GitHub \
  --git-branch main \
  --entrypoint-command 'bash -lc "python -m uv pip install --no-cache fastapi uvicorn && exec python -m uvicorn fastapiapp:app --host 0.0.0.0 --port \"$APP_PORT\""' \
  --app-port 8080 \
  --app-base-path /
```

```bash
hops app create flaskfromgithub \
  --app-kind CUSTOM \
  --git-url https://github.com/gibchikafa/appshopsworkstests.git \
  --git-provider GitHub \
  --git-branch main \
  --entrypoint-command 'bash -lc "python -m uv pip install --no-cache flask && exec python -m flask --app flaskapp run --host 0.0.0.0 --port \"$APP_PORT\""' \
  --app-port 8080 \
  --app-base-path /
```

```bash
hops app create gradiofromgithub \
  --app-kind CUSTOM \
  --git-url https://github.com/gibchikafa/appshopsworkstests.git \
  --git-provider GitHub \
  --git-branch main \
  --entrypoint-command 'bash -lc "python -m uv pip install --no-cache gradio && exec python gradioapp.py"' \
  --app-port 7860 \
  --app-base-path /
```

```bash
hops app create streamlitfromgithub \
  --app-kind STREAMLIT \
  --git-url https://github.com/gibchikafa/appshopsworkstests.git \
  --git-provider GitHub \
  --git-branch main \
  --entrypoint-script streamlitapp.py \
  --app-base-path /
```

Add `--start` if you want the CLI to start the app immediately after creation and wait for it to become serving.
