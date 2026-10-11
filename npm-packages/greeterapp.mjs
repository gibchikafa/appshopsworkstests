import express from "express";
import { greet, whereFrom } from "./src/greeter.js";

// A Node.js app for Hopsworks: created with app type Node.js and this file as the app file, it
// is started with `node npm-packages/greeterapp.mjs` and listens on PORT. The greeter comes from
// the clone next to this file; express, and the lodash and dayjs the greeter needs, resolve from
// the npm packages installed in the environment through the git import (see the README).
const port = Number(process.env.PORT || process.env.APP_PORT || 8080);
const host = process.env.HOST || "0.0.0.0";

const app = express();

app.get("/health", (req, res) => {
  res.json({ status: "ok" });
});

app.get("/", (req, res) => {
  res.type("html").send(`<!doctype html>
<html>
  <head>
    <meta charset="utf-8" />
    <title>Greeter on Hopsworks</title>
  </head>
  <body>
    <h1>${greet(req.query.name ?? "Hopsworks")}</h1>
    <p>Served at <code>${process.env.APP_PUBLIC_PATH ?? "/"}</code></p>
    <p>Greeter loaded from <code>${whereFrom()}</code></p>
  </body>
</html>`);
});

app.listen(port, host, () => {
  console.log(`Listening on http://${host}:${port}`);
});
