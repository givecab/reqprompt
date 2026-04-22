import sqlite3

from .constants import DB_PATH
from .questions import DEFAULT_QUESTIONS


def get_conn():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    with get_conn() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS projects (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                name          TEXT NOT NULL,
                client        TEXT NOT NULL,
                type          TEXT NOT NULL DEFAULT 'Software a medida',
                notes         TEXT NOT NULL DEFAULT '',
                generated_doc TEXT NOT NULL DEFAULT '',
                doc_date      TEXT NOT NULL DEFAULT '',
                created_at    TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS questions (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                category  TEXT NOT NULL,
                text      TEXT NOT NULL,
                q_type    TEXT NOT NULL DEFAULT 'Abierta',
                is_base   INTEGER NOT NULL DEFAULT 0
            );

            CREATE TABLE IF NOT EXISTS project_extra_questions (
                project_id  INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
                question_id INTEGER NOT NULL REFERENCES questions(id) ON DELETE CASCADE,
                PRIMARY KEY (project_id, question_id)
            );

            CREATE TABLE IF NOT EXISTS answers (
                project_id  INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
                question_id INTEGER NOT NULL REFERENCES questions(id) ON DELETE CASCADE,
                value       TEXT NOT NULL DEFAULT '',
                PRIMARY KEY (project_id, question_id)
            );
            """
        )

        count = conn.execute("SELECT COUNT(*) FROM questions WHERE is_base = 1").fetchone()[0]
        if count != len(DEFAULT_QUESTIONS):
            conn.execute("DELETE FROM questions WHERE is_base = 1")
            conn.executemany(
                "INSERT INTO questions (category, text, q_type, is_base) VALUES (?,?,?,?)",
                DEFAULT_QUESTIONS,
            )
