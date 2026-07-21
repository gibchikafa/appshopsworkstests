const express = require("express");

const PORT = process.env.APP_PORT || 8080;

const app = express();
const router = express.Router();

router.get("/health", (req, res) => {
  res.json({ status: "ok" });
});

router.get("/", (req, res) => {
  res.send(`<!doctype html>
<html>
  <head>
    <meta charset="utf-8" />
    <title>Express on Hopsworks</title>
  </head>
  <body>
    <h1>Express on Hopsworks</h1>
    <p>Route prefix: <code>/</code></p>
  </body>
</html>`);
});

app.use("/", router);

app.listen(PORT, "0.0.0.0", () => {
  console.log(`Listening on http://0.0.0.0:${PORT}`);
});
