import { createServer } from "node:http";
import pkg from "trino-client";

const { Trino, BasicAuth } = pkg;
const port = Number(process.env.APP_PORT || 8080);
const user = process.env.TRINO_USER;
const schema = process.env.TRINO_SCHEMA;
const featureGroup = process.env.FEATURE_GROUP_NAME || "customers";
const version = process.env.FEATURE_GROUP_VERSION || "1";

if (!process.env.TRINO_SERVER || !user || !schema) {
  throw new Error("Use start_trinoapp.py inside Hopsworks, or set TRINO_SERVER, TRINO_USER and TRINO_SCHEMA.");
}
if (!/^[1-9][0-9]*$/.test(version)) {
  throw new Error("FEATURE_GROUP_VERSION must be a positive integer.");
}
// Feature group customers, version 1, is exposed as table customers_1.
const tableName = `${featureGroup}_${version}`;
const quotedTable = '"' + tableName.replaceAll('"', '""') + '"';
const sql = `SELECT * FROM ${quotedTable} LIMIT 100`;

const trino = Trino.create({
  server: process.env.TRINO_SERVER,
  catalog: process.env.TRINO_CATALOG || "iceberg",
  schema,
  // Trino needs a user identity even when authentication is disabled.
  extraHeaders: { "X-Trino-User": user },
  ...(process.env.TRINO_PASSWORD
    ? { auth: new BasicAuth(user, process.env.TRINO_PASSWORD) }
    : {}),
});

async function queryFeatureGroup() {
  const query = await trino.query(sql);
  let columns = [];
  const rows = [];

  function collect(result) {
    // SQL errors can arrive in a result page with HTTP status 200.
    if (result.error) {
      throw new Error(`${result.error.errorName}: ${result.error.message}`);
    }
    if (result.columns) columns = result.columns;
    // Queued/running pages may not contain data yet.
    if (result.data) rows.push(...result.data);
  }

  // In trino-client 0.2.9 an immediate response can have done=true, which a
  // for-await loop skips. Inspect it explicitly so SQL errors are not hidden.
  const first = await query.next();
  if (first.value) collect(first.value);
  if (!first.done) {
    for await (const result of query) collect(result);
  }

  return { columns, rows, table: tableName };
}

const page = `<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Hopsworks feature group</title>
  <style>
    body { font: 16px system-ui, sans-serif; margin: 2rem; color: #17212b; }
    button { padding: .6rem 1rem; cursor: pointer; }
    .results { overflow-x: auto; }
    table { border-collapse: collapse; margin-top: 1rem; }
    th, td { padding: .6rem 1rem; border: 1px solid #ddd; text-align: left; }
    th { background: #f2f5f8; }
    #status { white-space: pre-wrap; }
  </style>
</head>
<body>
  <h1>Hopsworks feature group</h1>
  <p>Preview up to 100 offline rows from your configured feature group.</p>
  <button id="run">Load feature group</button>
  <p id="status" role="status">Ready.</p>
  <div class="results"><table id="results"></table></div>
  <script>
    const button = document.getElementById("run");
    const status = document.getElementById("status");
    const table = document.getElementById("results");

    button.addEventListener("click", async () => {
      button.disabled = true;
      status.textContent = "Querying Trino…";
      table.replaceChildren();
      try {
        // Keep the Hopsworks public URL prefix when calling the backend.
        const base = new URL(window.location.href);
        if (!base.pathname.endsWith("/")) base.pathname += "/";
        const response = await fetch(new URL("api/features", base));
        if (!response.ok) {
          const error = await response.json().catch(() => ({}));
          throw new Error(error.error || "HTTP " + response.status);
        }
        const { columns, rows, table: name } = await response.json();
        const header = table.createTHead().insertRow();
        for (const column of columns) {
          const cell = document.createElement("th");
          cell.textContent = column.name;
          header.appendChild(cell);
        }
        const body = table.createTBody();
        for (const row of rows) {
          const tr = body.insertRow();
          for (const value of row) {
            tr.insertCell().textContent = value === null ? "NULL"
              : typeof value === "object" ? JSON.stringify(value) : String(value);
          }
        }
        status.textContent = name + ": " + rows.length + " row(s) returned.";
      } catch (error) {
        status.textContent = "Query failed: " + error.message;
      } finally {
        button.disabled = false;
      }
    });
  </script>
</body>
</html>`;

function sendJson(res, code, body) {
  res.writeHead(code, {
    "Content-Type": "application/json; charset=utf-8",
    "Cache-Control": "no-store",
  });
  res.end(JSON.stringify(body));
}

createServer(async (req, res) => {
  const path = req.url.split("?")[0];
  if (req.method !== "GET") {
    res.setHeader("Allow", "GET");
    return sendJson(res, 405, { error: "Method not allowed" });
  }
  if (path === "/health") return sendJson(res, 200, { status: "ok" });
  if (path === "/") {
    res.writeHead(200, { "Content-Type": "text/html; charset=utf-8" });
    return res.end(page);
  }
  if (path === "/api/features") {
    try {
      return sendJson(res, 200, await queryFeatureGroup());
    } catch (error) {
      // Log just the message: HTTP error objects can include credentials.
      console.error("Trino query failed:", error.message);
      return sendJson(res, 502, { error: error.message });
    }
  }
  sendJson(res, 404, { error: "Not found" });
}).listen(port, "0.0.0.0", () => {
  console.log(`Trino example listening on 0.0.0.0:${port}`);
});
