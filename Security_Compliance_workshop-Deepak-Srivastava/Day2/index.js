const express = require("express");
const sqlite3 = require("sqlite3").verbose();
const app = express();
const port = 3000;

// Setup in-memory SQLite DB
let db = new sqlite3.Database(":memory:");
db.serialize(() => {
  db.run("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, password TEXT)");
  db.run("INSERT INTO users (name, password) VALUES ('admin', 'supersecret')");
});

// ❌ Vulnerable to SQL Injection
app.get("/", (req, res) => {
  res.send("Hello World");
});

app.get("/user", (req, res) => {
  const userId = req.query.id; // unvalidated
  const query = `SELECT * FROM users WHERE id = '${userId}'`;
  console.log("Executing:", query);
  db.get(query, (err, row) => {
    if (err) res.status(500).send(err.message);
    else res.send(row ? row : "No user found");
  });
});

// ❌ Vulnerable to Reflected XSS
app.get("/search", (req, res) => {
  const q = req.query.q || "";
  res.send(`<h1>Results for: ${q}</h1>`); // directly reflected
});

app.listen(port, () => {
  console.log(`🚨 Vulnerable app running at http://localhost:${port}`);
});
