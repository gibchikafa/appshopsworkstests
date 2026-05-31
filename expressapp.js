const express = require("express");

const APP_BASE_URL_PATH = (process.env.APP_BASE_URL_PATH || "").replace(/\/+$/, "");
const PORT = process.env.APP_PORT || 8080;

const app = express();
const router = express.Router();

router.get("/health", (req, res) => {
  res.json({ status: "ok" });
});

router.get("/", (req, res) => {
  const base = APP_BASE_URL_PATH || "/";
  res.send(`<!doctype html>
<html>
  <head>
    <meta charset="utf-8" />
    <title>Express on Hopsworks</title>
  </head>
  <body>
    <h1>Express on Hopsworks</h1>
    <p>Base path: <code>${base}</code></p>
  </body>
</html>`);
});

app.use(APP_BASE_URL_PATH || "/", router);

app.listen(PORT, "0.0.0.0", () => {
  console.log(`Listening on http://0.0.0.0:${PORT}${APP_BASE_URL_PATH || ""}`);
});
