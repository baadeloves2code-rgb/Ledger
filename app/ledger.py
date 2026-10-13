import os
import sqlite3
import time

from flask import Flask, g, jsonify, request

DB_PATH = os.environ.get("LEDGER_DB", "/var/lib/ledger/ledger.db")
app = Flask(__name__)


def db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.execute(
            "CREATE TABLE IF NOT EXISTS expenses ("
            "id INTEGER PRIMARY KEY, amount_cents INTEGER NOT NULL, "
            "note TEXT, created REAL)"
        )
    return g.db


@app.teardown_appcontext
def close_db(_exc):
    conn = g.pop("db", None)
    if conn is not None:
        conn.close()


@app.get("/health")
def health():
    try:
        db().execute("SELECT 1")
        return jsonify(status="ok")
    except sqlite3.Error as e:
        return jsonify(status="error", detail=str(e)), 503


@app.get("/expenses")
def list_expenses():
    rows = db().execute("SELECT id, amount_cents, note FROM expenses ORDER BY id").fetchall()
    return jsonify([{"id": r[0], "amount_cents": r[1], "note": r[2]} for r in rows])


@app.post("/expenses")
def add_expense():
    body = request.get_json(force=True)
    conn = db()
    cur = conn.execute(
        "INSERT INTO expenses (amount_cents, note, created) VALUES (?, ?, ?)",
        (int(body["amount_cents"]), body.get("note", ""), time.time()),
    )
    conn.commit()
    return jsonify(id=cur.lastrowid), 201


@app.get("/slow")
def slow():
    # For timeout drills: /slow?s=10 waits 10 seconds before answering.
    time.sleep(float(request.args.get("s", 5)))
    return jsonify(slept=True)
