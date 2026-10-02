"""Load Hopsworks Trino credentials, then replace this process with Node.js."""

import os
from pathlib import Path

import hopsworks


project = hopsworks.login()
trino_api = project.get_trino_api()
user, password = trino_api.get_basic_auth()

env = os.environ.copy()
env["TRINO_SERVER"] = f"https://{trino_api.get_host()}:{trino_api.get_port()}"
env["TRINO_USER"] = user
env["TRINO_PASSWORD"] = password
env.setdefault("TRINO_CATALOG", "iceberg")
env.setdefault("TRINO_SCHEMA", project.name.lower())

# The in-cluster Hopsworks client uses this CA bundle. Node reads this variable
# at startup. A supplied NODE_EXTRA_CA_CERTS takes precedence.
if "NODE_EXTRA_CA_CERTS" not in env and Path("/tmp/ca_chain.pem").is_file():
    env["NODE_EXTRA_CA_CERTS"] = "/tmp/ca_chain.pem"

# Credentials are passed in the process environment, never printed or written
# into the repository. Every data query is executed by the JavaScript app.
app_file = Path(__file__).with_name("trinoapp.mjs")
os.execvpe("node", ["node", str(app_file)], env)
